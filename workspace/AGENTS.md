# Agent Instructions

This file defines operational rules for agents running inside **mybot**.

---

## Scope

- Operate only within verified capabilities
- Do not assume tools, files, or features exist
- Inspect the environment before relying on anything

---

## Tools & capabilities

Built-in Tools can be found in `TOOLS.md`

Built-in Skills can be found in `skills`

---

## Memory model

mybot uses file-based memory:

- `memory/HISTORY.md` — temporal event log
- `memory/MEMORY.md` — sparse, long-term memory (promotion-only)

Do not claim memory unless information exists in these files.
USER.md is read-only and must not be modified.

---

## Scheduled reminders

One-time reminders must use the scheduler:

mybot cron add --name "reminder" --message "TEXT" --at "YYYY-MM-DDTHH:MM:SS" --deliver --to "USER_ID" --channel "CHANNEL"

Do not write reminders to MEMORY.md.

---

## Heartbeat

`HEARTBEAT.md` is checked periodically.

- High-priority tasks only
- Skip if empty (comments or headers only)
