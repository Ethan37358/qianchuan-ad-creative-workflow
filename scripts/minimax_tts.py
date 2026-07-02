#!/usr/bin/env python3
"""
Generate voiceover audio through MiniMax TTS.

Environment variables:
  MINIMAX_API_KEY
  MINIMAX_GROUP_ID

Common optional variables:
  MINIMAX_TTS_MODEL (default: speech-02-hd)
  MINIMAX_TTS_VOICE_ID (default: Chinese (Mandarin)_Warm_Girl)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

from env_loader import load_env


def parse_audio_payload(data: dict[str, Any]) -> bytes:
    # MiniMax response formats can differ by endpoint version. Support common shapes:
    # {"data":{"audio":"<hex or base64>"}} or {"audio_file":"..."}.
    candidates = [
        data.get("audio"),
        data.get("audio_file"),
        (data.get("data") or {}).get("audio"),
        (data.get("data") or {}).get("audio_file"),
    ]
    audio_value = next((c for c in candidates if isinstance(c, str) and c), None)
    if not audio_value:
        raise ValueError(f"No audio payload found in response: {json.dumps(data, ensure_ascii=False)[:800]}")

    cleaned = audio_value.strip()
    if re.fullmatch(r"[0-9a-fA-F]+", cleaned) and len(cleaned) % 2 == 0:
        return bytes.fromhex(cleaned)
    return base64.b64decode(cleaned)


def minimax_tts(text: str, output: Path, voice_id: str, model: str, speed: float, vol: float, pitch: int) -> None:
    api_key = os.getenv("MINIMAX_API_KEY")
    group_id = os.getenv("MINIMAX_GROUP_ID")
    if not api_key:
        missing = [k for k, v in {"MINIMAX_API_KEY": api_key}.items() if not v]
        raise RuntimeError("Missing MiniMax credentials: " + ", ".join(missing))

    url = "https://api.minimax.chat/v1/t2a_v2"
    if group_id:
        url = f"{url}?GroupId={group_id}"
    body = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    audio = parse_audio_payload(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(audio)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--voice-id", default=os.getenv("MINIMAX_TTS_VOICE_ID", "Chinese (Mandarin)_Warm_Girl"))
    parser.add_argument("--model", default=os.getenv("MINIMAX_TTS_MODEL", "speech-02-hd"))
    parser.add_argument("--speed", type=float, default=1.08)
    parser.add_argument("--vol", type=float, default=1.0)
    parser.add_argument("--pitch", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--env", type=Path, help="Path to .env file. Defaults to searching current project and skill folder.")
    args = parser.parse_args()
    env_path = load_env(args.env)

    if args.voice_id == "Chinese (Mandarin)_Warm_Girl":
        args.voice_id = os.getenv("MINIMAX_TTS_VOICE_ID", args.voice_id)
    if args.model == "speech-02-hd":
        args.model = os.getenv("MINIMAX_TTS_MODEL", args.model)

    text = args.text.read_text(encoding="utf-8").strip()
    if args.dry_run:
        print(json.dumps({
            "text_file": str(args.text),
            "output": str(args.out),
            "env_file": str(env_path) if env_path else None,
            "model": args.model,
            "voice_id": args.voice_id,
            "speed": args.speed,
            "vol": args.vol,
            "pitch": args.pitch,
            "missing_keys": [k for k in ("MINIMAX_API_KEY", "MINIMAX_GROUP_ID") if not os.getenv(k)],
            "required_keys": ["MINIMAX_API_KEY"],
            "optional_but_common_keys": ["MINIMAX_GROUP_ID"],
            "chars": len(text),
        }, ensure_ascii=False, indent=2))
        return 0

    try:
        minimax_tts(text, args.out, args.voice_id, args.model, args.speed, args.vol, args.pitch)
    except Exception as exc:
        print(f"MiniMax TTS failed: {exc}", file=sys.stderr)
        return 1
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
