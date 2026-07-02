#!/usr/bin/env python3
"""
Unified runner for the Qianchuan ad creative workflow.

This runner intentionally keeps the "agent reasoning" parts outside the script:
creative strategy,口播 writing, storyboard quality, and compliance judgment should
be produced or reviewed by the agent. The script handles repeatable plumbing:
configuration checks, template creation, network material collection, and MiniMax TTS.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from env_loader import load_env


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent


def key_status(keys: list[str]) -> dict[str, str]:
    return {key: "set" if os.getenv(key) else "missing" for key in keys}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def copy_template(template_name: str, out: Path) -> None:
    src = SKILL_ROOT / "assets" / template_name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def run_command(cmd: list[str]) -> int:
    print("Running:", " ".join(cmd), file=sys.stderr)
    return subprocess.call(cmd)


def check(args: argparse.Namespace) -> int:
    env_path = load_env(args.env)
    scripts = {
        "material_collector": SCRIPT_DIR / "material_collector.py",
        "minimax_tts": SCRIPT_DIR / "minimax_tts.py",
    }
    report = {
        "skill_root": str(SKILL_ROOT),
        "env_file": str(env_path) if env_path else None,
        "scripts": {name: path.exists() for name, path in scripts.items()},
        "keys": key_status([
            "PEXELS_API_KEY",
            "PIXABAY_API_KEY",
            "COVERR_API_KEY",
            "MINIMAX_API_KEY",
            "MINIMAX_GROUP_ID",
        ]),
        "notes": [
            "Planning,口播 writing, and storyboard generation can run without API keys.",
            "Network material collection requires provider keys.",
            "MiniMax TTS requires MINIMAX_API_KEY; some accounts also require MINIMAX_GROUP_ID.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def init_project(args: argparse.Namespace) -> int:
    project_dir = args.project_dir.resolve()
    project_dir.mkdir(parents=True, exist_ok=True)
    copy_template("brief-template.json", project_dir / "brief.json")
    copy_template("storyboard-template.json", project_dir / "storyboard.json")
    env_example = SKILL_ROOT / ".env.example"
    if not (project_dir / ".env").exists():
        (project_dir / ".env").write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")
    print(project_dir)
    return 0


def collect_materials(args: argparse.Namespace) -> int:
    load_env(args.env)
    out = args.out or (args.project_dir / "material_candidates.json")
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "material_collector.py"),
        "--storyboard",
        str(args.storyboard),
        "--out",
        str(out),
        "--providers",
        args.providers,
        "--per-provider",
        str(args.per_provider),
    ]
    if args.download:
        cmd.append("--download")
        cmd.extend(["--download-dir", str(args.download_dir or (args.project_dir / "network_materials"))])
    if args.env:
        cmd.extend(["--env", str(args.env)])
    return run_command(cmd)


def tts(args: argparse.Namespace) -> int:
    load_env(args.env)
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "minimax_tts.py"),
        "--text",
        str(args.text),
        "--out",
        str(args.out),
        "--speed",
        str(args.speed),
    ]
    if args.voice_id:
        cmd.extend(["--voice-id", args.voice_id])
    if args.model:
        cmd.extend(["--model", args.model])
    if args.dry_run:
        cmd.append("--dry-run")
    if args.env:
        cmd.extend(["--env", str(args.env)])
    return run_command(cmd)


def summarize_brief(args: argparse.Namespace) -> int:
    brief = read_json(args.brief)
    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": brief.get("mode"),
        "material_source": brief.get("material_source"),
        "voice_source": brief.get("voice_source"),
        "product": brief.get("product"),
        "campaign_goal": brief.get("campaign_goal"),
        "required_next_agent_steps": [
            "Generate product assumptions and risk map.",
            "Generate creative matrix.",
            "Generate timed voiceover and subtitle script.",
            "Generate storyboard JSON.",
            "Run material collection if network/hybrid is selected.",
            "Run MiniMax TTS if minimax voice is selected.",
            "Assemble video using local environment tools or export an editing package.",
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path)
    parser.add_argument("--check", action="store_true")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init-project")
    init_parser.add_argument("project_dir", type=Path)

    collect_parser = subparsers.add_parser("collect-materials")
    collect_parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    collect_parser.add_argument("--storyboard", type=Path, required=True)
    collect_parser.add_argument("--out", type=Path)
    collect_parser.add_argument("--providers", default="pexels,pixabay,coverr")
    collect_parser.add_argument("--per-provider", type=int, default=3)
    collect_parser.add_argument("--download", action="store_true")
    collect_parser.add_argument("--download-dir", type=Path)

    tts_parser = subparsers.add_parser("tts")
    tts_parser.add_argument("--text", type=Path, required=True)
    tts_parser.add_argument("--out", type=Path, required=True)
    tts_parser.add_argument("--voice-id")
    tts_parser.add_argument("--model")
    tts_parser.add_argument("--speed", type=float, default=1.08)
    tts_parser.add_argument("--dry-run", action="store_true")

    summarize_parser = subparsers.add_parser("summarize-brief")
    summarize_parser.add_argument("--brief", type=Path, required=True)

    args = parser.parse_args()
    if args.check:
        return check(args)
    if args.command == "init-project":
        return init_project(args)
    if args.command == "collect-materials":
        return collect_materials(args)
    if args.command == "tts":
        return tts(args)
    if args.command == "summarize-brief":
        return summarize_brief(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
