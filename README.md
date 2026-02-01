# Access Control & Operations Logging System

## Overview
A menu-driven Python application that simulates an internal access control system used in secure operational environments.  
The system manages registered users, applies rule-based access decisions, and maintains a persistent audit log of all access attempts.

This project was built to demonstrate core software engineering fundamentals, system design thinking, and real-world operational logic.

---

## Key Features
- Register people, vehicles, and contractors
- Rule-based access decisions (GRANT / DENY)
- Time-based access restrictions for contractors (06:00–20:00)
- Persistent data storage using JSON files
- Full audit logging with timestamps and decision reasons
- Flagging of repeated denied access attempts
- Export of access logs to CSV for reporting and audits

---

## System Design
- Menu-driven command-line interface
- Clear separation of responsibilities (decision logic, storage, utilities)
- Deterministic access rules with explicit reasoning
- Defensive handling of unknown or invalid IDs
- Persistent state across application runs

---

## What This Demonstrates
- Structured program design
- Logical decision-making and rule enforcement
- File handling and data persistence
- Audit and reporting considerations
- Real-world system thinking around security and operations
- Debugging and iterative development

---

## Technologies Used
- Python 3
- JSON (data persistence)
- CSV (reporting/export)

---

## How to Run
```bash
python main.py
