from __future__ import annotations
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent / "data"
USERS_PATH = DATA_DIR / "users.json"
LOGS_PATH = DATA_DIR / "logs.json"

def _ensure_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for path in (USERS_PATH, LOGS_PATH):
        if not path.exists():
            path.write_text("[]", encoding="utf-8")

def load_json(path: Path) -> list[dict[str, Any]]:
    _ensure_files()
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    return json.loads(raw)

def save_json(path: Path, data: list[dict[str, Any]]) -> None:
    _ensure_files()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_users() -> list[dict[str, Any]]:
    return load_json(USERS_PATH)

def save_users(users: list[dict[str, Any]]) -> None:
    save_json(USERS_PATH, users)

def load_logs() -> list[dict[str, Any]]:
    return load_json(LOGS_PATH)

def save_logs(logs: list[dict[str, Any]]) -> None:
    save_json(LOGS_PATH, logs)
