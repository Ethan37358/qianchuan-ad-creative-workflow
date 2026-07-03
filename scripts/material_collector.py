#!/usr/bin/env python3
"""
Collect material candidates for Qianchuan storyboard scenes.

Inputs:
  --storyboard JSON file with scenes:
    [{"scene": 1, "query_cn": "...", "query_en": "...", "need": "..."}]

Environment variables:
  PEXELS_API_KEY
  PIXABAY_API_KEY
  COVERR_API_KEY (optional; Coverr availability depends on account/API access)

Outputs:
  candidates JSON and optional downloads.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from env_loader import load_env


def request_json(url: str, headers: dict[str, str] | None = None, timeout: int = 30) -> dict[str, Any]:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def safe_name(value: str, max_len: int = 80) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", value.strip())
    return value[:max_len].strip("_") or "asset"


def download(url: str, path: Path, timeout: int = 60) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "qianchuan-material-collector/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        path.write_bytes(resp.read())


def pexels_video_search(query: str, per_page: int) -> list[dict[str, Any]]:
    key = os.getenv("PEXELS_API_KEY")
    if not key:
        return []
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": query, "orientation": "portrait", "per_page": per_page}
    )
    data = request_json(url, headers={"Authorization": key})
    results = []
    for item in data.get("videos", []):
        files = item.get("video_files", [])
        vertical_files = [
            f for f in files
            if f.get("width") and f.get("height") and int(f["height"]) >= int(f["width"])
        ]
        selected = sorted(
            vertical_files or files,
            key=lambda f: int(f.get("width") or 0) * int(f.get("height") or 0),
            reverse=True,
        )
        file_obj = selected[0] if selected else {}
        results.append({
            "provider": "pexels",
            "id": item.get("id"),
            "query": query,
            "url": item.get("url"),
            "download_url": file_obj.get("link"),
            "width": file_obj.get("width"),
            "height": file_obj.get("height"),
            "duration": item.get("duration"),
            "author": (item.get("user") or {}).get("name"),
            "license_note": "Verify current Pexels license before real ad launch.",
        })
    return results


def pixabay_video_search(query: str, per_page: int) -> list[dict[str, Any]]:
    key = os.getenv("PIXABAY_API_KEY")
    if not key:
        return []
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": key, "q": query, "video_type": "all", "orientation": "vertical", "per_page": per_page}
    )
    data = request_json(url)
    results = []
    for item in data.get("hits", []):
        videos = item.get("videos") or {}
        selected = videos.get("large") or videos.get("medium") or videos.get("small") or videos.get("tiny") or {}
        results.append({
            "provider": "pixabay",
            "id": item.get("id"),
            "query": query,
            "url": item.get("pageURL"),
            "download_url": selected.get("url"),
            "width": selected.get("width"),
            "height": selected.get("height"),
            "duration": item.get("duration"),
            "author": item.get("user"),
            "license_note": "Verify current Pixabay license before real ad launch.",
        })
    return results


def coverr_video_search(query: str, per_page: int) -> list[dict[str, Any]]:
    key = os.getenv("COVERR_API_KEY")
    if not key:
        return []
    # Coverr has changed public API availability over time. Keep this isolated so it can be
    # adjusted after the user's account/API docs are confirmed.
    url = "https://api.coverr.co/videos?" + urllib.parse.urlencode({"query": query, "page_size": per_page})
    try:
        data = request_json(url, headers={"Authorization": f"Bearer {key}"})
    except Exception as exc:
        return [{
            "provider": "coverr",
            "query": query,
            "error": f"Coverr request failed; confirm account API endpoint/authorization: {exc}",
        }]
    raw_items = data.get("videos") or data.get("results") or data.get("items") or []
    results = []
    for item in raw_items:
        results.append({
            "provider": "coverr",
            "id": item.get("id"),
            "query": query,
            "url": item.get("url") or item.get("coverr_url"),
            "download_url": item.get("download_url") or item.get("video_url"),
            "width": item.get("width"),
            "height": item.get("height"),
            "duration": item.get("duration"),
            "author": item.get("author"),
            "license_note": "Verify current Coverr terms before real ad launch.",
        })
    return results


def load_storyboard(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data.get("scenes", [])
    if isinstance(data, list):
        return data
    raise ValueError("Storyboard JSON must be a list or an object with scenes.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--download-dir", type=Path)
    parser.add_argument("--per-provider", type=int, default=3)
    parser.add_argument("--providers", default="pexels,pixabay,coverr")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--env", type=Path, help="Path to .env file. Defaults to searching current project and skill folder.")
    args = parser.parse_args()
    env_path = load_env(args.env)

    providers = [p.strip().lower() for p in args.providers.split(",") if p.strip()]
    scenes = load_storyboard(args.storyboard)
    output = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": str(env_path) if env_path else None,
        "missing_keys": [
            key for key in ("PEXELS_API_KEY", "PIXABAY_API_KEY", "COVERR_API_KEY")
            if key.split("_")[0].lower() in providers and not os.getenv(key)
        ],
        "scenes": [],
    }

    for scene in scenes:
        query = scene.get("query_en") or scene.get("query") or scene.get("query_cn") or scene.get("need") or ""
        scene_result = {"scene": scene, "candidates": []}
        if "pexels" in providers:
            scene_result["candidates"].extend(pexels_video_search(query, args.per_provider))
        if "pixabay" in providers:
            scene_result["candidates"].extend(pixabay_video_search(query, args.per_provider))
        if "coverr" in providers:
            scene_result["candidates"].extend(coverr_video_search(query, args.per_provider))

        if args.download and args.download_dir:
            for idx, candidate in enumerate(scene_result["candidates"], 1):
                url = candidate.get("download_url")
                if not url:
                    continue
                ext = ".mp4"
                filename = f"scene_{scene.get('scene', 'x')}_{idx}_{candidate.get('provider')}_{safe_name(query)}{ext}"
                path = args.download_dir / filename
                try:
                    download(url, path)
                    candidate["local_path"] = str(path)
                except Exception as exc:
                    candidate["download_error"] = str(exc)

        output["scenes"].append(scene_result)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.out)
    if env_path:
        print(f"Loaded env: {env_path}", file=sys.stderr)
    if output["missing_keys"]:
        print("Missing keys:", ", ".join(output["missing_keys"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
