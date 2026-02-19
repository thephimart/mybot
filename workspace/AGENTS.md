# Agent Instructions

This file defines operational rules for agents running inside **mybot**.

---

## Scope

- Operate only within verified capabilities
- Do not assume tools, files, or features exist
- **Always check TOOLS.md and skills/ directory first** before claiming you can perform a task
- If a tool isn't documented, it may not exist — ask the user or check the source

---

## Tools & capabilities

**Always refer to `workspace/TOOLS.md` for the complete, authoritative list of available tools.**

Built-in Tools can be found in `TOOLS.md`

Built-in Skills can be found in `skills/` (builtin) or `workspace/skills/` (workspace overrides)

Skills are markdown files that teach the agent how to use specific tools or perform certain tasks. Some skills require external dependencies (CLI tools, environment variables) — check skill metadata for requirements.

---

## Memory model

mybot uses file-based memory:

- `memory/HISTORY.md` — temporal event log
- `memory/MEMORY.md` — sparse, long-term memory (promotion-only)

Do not claim memory unless information exists in these files.
USER.md is read-only and must not be modified.

---

## Scheduled reminders

Use the `mybot cron` CLI command:

```bash
# Recurring
mybot cron add --name "reminder" --message "TEXT" --cron "0 9 * * *"
mybot cron add --name "reminder" --message "TEXT" --every 7200

# One-time
mybot cron add --name "reminder" --message "TEXT" --at "2026-02-12T10:30:00"

# Manage
mybot cron list
mybot cron remove <job_id>
```

Do not write reminders to MEMORY.md.

---

## Heartbeat

`HEARTBEAT.md` is checked periodically (every 30 minutes in gateway mode).

- High-priority tasks only
- Skip if empty (comments or headers only)
- **Note:** Only active when running `mybot gateway`, not in direct chat mode
