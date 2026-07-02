from __future__ import annotations

import os
from pathlib import Path


def parse_env_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key, value


def find_env_file(explicit: str | Path | None = None) -> Path | None:
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.exists() else None

    candidates: list[Path] = []
    cwd = Path.cwd().resolve()
    candidates.extend([cwd / ".env", cwd / ".qianchuan.env"])
    candidates.extend(parent / ".env" for parent in list(cwd.parents)[:5])

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    candidates.extend([
        skill_root / ".env",
        skill_root / ".qianchuan.env",
        skill_root / "config" / ".env",
    ])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    return None


def load_env(explicit: str | Path | None = None) -> Path | None:
    path = find_env_file(explicit)
    if not path:
        return None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        parsed = parse_env_line(raw_line)
        if not parsed:
            continue
        key, value = parsed
        os.environ.setdefault(key, value)
    return path
