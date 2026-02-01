from __future__ import annotations
from datetime import datetime, timezone

def now_iso() -> str:
    """Return current time in ISO-8601 format (UTC)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def safe_input(prompt: str) -> str:
    """Input wrapper to avoid accidental leading/trailing spaces."""
    return input(prompt).strip()

def press_enter() -> None:
    input("\nPress Enter to continue...")