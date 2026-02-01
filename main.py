from __future__ import annotations

import csv
from datetime import datetime
from typing import Any

from utils import now_iso, safe_input, press_enter
from storage import load_users, save_users, load_logs, save_logs


# -----------------------------
# Helpers
# -----------------------------

def find_user(users: list[dict[str, Any]], user_id: str) -> dict[str, Any] | None:
    for u in users:
        if u.get("id") == user_id:
            return u
    return None


def add_log(logs: list[dict[str, Any]], event: dict[str, Any]) -> None:
    logs.append(event)


def count_recent_denies(logs: list[dict[str, Any]], user_id: str, last_n: int = 5) -> int:
    recent = [e for e in logs if e.get("user_id") == user_id][-last_n:]
    return sum(1 for e in recent if e.get("decision") == "DENY")


def within_hours(start_h: int, end_h: int) -> bool:
    """Return True if current local hour is within [start_h, end_h)."""
    hour = datetime.now().hour
    return start_h <= hour < end_h


def decide_access(user: dict[str, Any] | None) -> tuple[str, str]:
    """
    Return (decision, reason).
    Rules:
    - Unknown ID: DENY
    - contractor: GRANT only 06:00–20:00 (local time)
    - person/vehicle/other: GRANT
    """
    if not user:
        return "DENY", "Unknown ID"

    utype = (user.get("type") or "person").lower()

    if utype == "contractor":
        if within_hours(6, 20):
            return "GRANT", "Contractor within permitted hours (06:00–20:00)"
        return "DENY", "Contractor outside permitted hours (06:00–20:00)"

    return "GRANT", "Valid ID"


def export_logs_to_csv(logs: list[dict[str, Any]]) -> None:
    """Export audit logs to a timestamped CSV in the project folder."""
    if not logs:
        print("No logs to export.")
        return

    filename = f"access_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "user_id", "name", "type", "decision", "reason", "flag"]
        )
        writer.writeheader()
        for entry in logs:
            writer.writerow({
                "timestamp": entry.get("timestamp", ""),
                "user_id": entry.get("user_id", ""),
                "name": entry.get("name", ""),
                "type": entry.get("type", ""),
                "decision": entry.get("decision", ""),
                "reason": entry.get("reason", ""),
                "flag": entry.get("flag", ""),
            })

    print(f"Logs exported to {filename}")


# -----------------------------
# Core actions
# -----------------------------

def register_user(users: list[dict[str, Any]]) -> None:
    print("\n--- Register person/vehicle ---")
    user_id = safe_input("Create an ID (e.g. A123): ").upper()

    if not user_id:
        print("ID cannot be empty.")
        return

    if find_user(users, user_id):
        print("That ID already exists.")
        return

    name = safe_input("Name (person/vehicle label): ")
    utype = safe_input("Type (person/vehicle/contractor): ").lower() or "person"

    users.append({
        "id": user_id,
        "name": name,
        "type": utype,
        "created_at": now_iso()
    })

    print(f"Registered: {user_id} ({name})")


def request_access(users: list[dict[str, Any]], logs: list[dict[str, Any]]) -> None:
    print("\n--- Access request ---")
    user_id = safe_input("Enter ID: ").upper()
    user = find_user(users, user_id)

    decision, reason = decide_access(user)
    name = user.get("name", "") if user else ""
    utype = user.get("type", "") if user else ""

    event: dict[str, Any] = {
        "timestamp": now_iso(),
        "user_id": user_id,
        "name": name,
        "type": utype,
        "decision": decision,
        "reason": reason
    }

    add_log(logs, event)

    # Flag unusual pattern: 3+ denies in last 5 attempts for same ID
    if decision == "DENY":
        denies = count_recent_denies(logs, user_id, last_n=5)
        if denies >= 3:
            event["flag"] = "Repeated denies (3+ of last 5)"
            print("⚠️ Flag raised: repeated denied attempts.")

    print(f"Decision: {decision} | Reason: {reason}")


def view_users(users: list[dict[str, Any]]) -> None:
    print("\n--- Registered users ---")
    if not users:
        print("No users registered yet.")
        return

    for u in users:
        print(f"- {u.get('id','')} | {u.get('name','')} | {u.get('type','')} | created {u.get('created_at','')}")


def view_logs(logs: list[dict[str, Any]]) -> None:
    print("\n--- Access logs ---")
    if not logs:
        print("No logs yet.")
        return

    choice = safe_input("Filter? (all/id/denied) [all]: ").lower() or "all"
    items = logs

    if choice == "id":
        uid = safe_input("Enter ID to filter: ").upper()
        items = [e for e in logs if e.get("user_id") == uid]
    elif choice == "denied":
        items = [e for e in logs if e.get("decision") == "DENY"]

    for e in items:
        flag = f" | FLAG: {e['flag']}" if "flag" in e else ""
        print(f"{e.get('timestamp','')} | {e.get('user_id','')} | {e.get('decision','')} | {e.get('reason','')}{flag}")


# -----------------------------
# Menu
# -----------------------------

def menu() -> None:
    users = load_users()
    logs = load_logs()

    while True:
        print("\n==============================")
        print(" Access Control & Ops Logger ")
        print("==============================")
        print("1) Register person/vehicle")
        print("2) Request access (grant/deny)")
        print("3) View registered users")
        print("4) View access logs")
        print("5) Export logs to CSV")
        print("6) Exit")

        choice = safe_input("Choose an option: ")

        if choice == "1":
            register_user(users)
            save_users(users)
            press_enter()

        elif choice == "2":
            request_access(users, logs)
            save_logs(logs)
            press_enter()

        elif choice == "3":
            view_users(users)
            press_enter()

        elif choice == "4":
            view_logs(logs)
            press_enter()

        elif choice == "5":
            export_logs_to_csv(logs)
            press_enter()

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()
