# nanobot → mybot Refactor Summary

## Overview

The nanobot codebase was heavily refactored into **mybot** — a minimal, fork-first, pure-Python bot core. All external integrations were removed, Docker support was deleted, and the project was stripped to its fundamentals.

---

## What Was Removed

### Channels Deleted
- Discord (`discord.py`)
- Slack (`slack.py`)
- WhatsApp (`whatsapp.py`)
- DingTalk (`dingtalk.py`)
- Feishu (`feishu.py`)
- QQ (`qq.py`)
- Mochat (`mochat.py`)

### Remaining Channels
- Telegram
- Email

### Other Deletions
- `bridge/` — entire TypeScript/Node.js directory (was only for WhatsApp)
- `Dockerfile`
- `.dockerignore`
- `COMMUNICATIONS.md` (deleted by user)

### Dependencies Removed
- `dingtalk-stream`
- `lark-oapi`
- `slack-sdk`
- `slackify-markdown`
- `qq-botpy`
- `python-socks`

---

## Files Modified

### Configuration
- `nanobot/config/schema.py` — Removed channel config classes for deleted channels

### Channels
- `nanobot/channels/manager.py` — Simplified to load only telegram and email
- `nanobot/channels/base.py` — Updated docstring

### CLI
- `nanobot/cli/commands.py` — Removed channel status display, removed `channels login` command, removed `_get_bridge_dir()` function

### Comments Updated (WhatsApp references removed)
- `nanobot/cron/types.py`
- `nanobot/bus/events.py`
- `nanobot/agent/tools/message.py`
- `nanobot/agent/context.py`

### Project Config
- `pyproject.toml` — Removed unused dependencies, removed bridge from build config

### Documentation
- `README.md` — Complete rewrite by user
- `SECURITY.md` — Complete rewrite by user

---

## Files Created

- `AGENTS.md` — Agent instructions for coding on the project (environment setup, commands, code style)
- `.venv/` — Python virtual environment

---

## Technical Changes

1. **No more Node.js** — Project is now pure Python 3.11+
2. **No Docker** — Removed container deployment files
3. **Minimal channels** — Only Telegram and Email remain
4. **Fork-first philosophy** — Code explicitly designed to be copied, renamed, and modified

---

## User's Documentation Rewrite

### README.md (by user)

The user completely rewrote README.md with a new philosophy:

- **Project renamed** from "nanobot" to "mybot"
- **Core message**: A minimal bot core, not a framework
- **Pure Python**: No Node, npm, or JS runtime
- **Deliberately small** and readable
- **Designed to be forked**, not extended via plugins
- **Agent-first**, not chat-first

Key sections:
- What mybot is (core, not framework; pure Python; fork-first)
- What mybot is not (batteries-included, platform, SaaS)
- Design philosophy (minimal surface area, fork-first, explicit over configurable, security by reduction)
- Included functionality (agent loop, tools, memory, scheduling, Telegram, Email, CLI)
- Project structure (agent/, tools/, channels/, cron/, bus/, providers/, config/, cli/)
- How to use (git clone → rename → delete → build)
- Line count (intentionally small)
- Origin & attribution (fork of nanobot, MIT license)

### SECURITY.md (by user)

The user rewrote SECURITY.md with a local-first, fork-first security model:

- **No hosted service** — You are responsible for your deployment
- **Threat model** — Assumes you run on a machine you control, trust the user account, review code
- **API keys** — Never commit secrets, use restricted permissions, rotate regularly
- **Tool execution** — Review every enabled tool, never run as root
- **File system** — Not a sandbox, use OS-level permissions
- **Network** — Use HTTPS, apply firewalls, monitor traffic
- **Dependencies** — Use pip-audit, remove unused deps
- **Channels** — Restrict access, log attempts, remove unused channels
- **Logs** — May contain sensitive data, protect with permissions
- **Known limitations** — No rate limiting, auth frameworks, encrypted storage, session expiry, audit trails
- **Incident response** — Your responsibility (revoke keys, stop bot, review logs, rotate creds, patch, re-deploy)

Philosophy: Security comes from minimal code, explicit behavior, local control, and informed operators.

---

## Current State

The project is now:
- ~4,000 lines of Python code
- Pure Python 3.11+ (no Node.js)
- No Docker
- No git connection
- Two channels: Telegram and Email
- Version 0.1.0
- Ready to fork and customize

---

## Additional Changes

### Directory & Import Renaming
- Renamed `nanobot/` → `mybot/` (entire directory)
- Replaced all `from nanobot.` imports with `from mybot.` throughout Python files

### Project Config Updates
- Updated `pyproject.toml`: package name, entry points, build config (all `nanobot` → `mybot`)
- Updated version from `0.1.3.post7` to `0.1.0`
- Removed bridge/ from build config in pyproject.toml
- Updated AGENTS.md with all nanobot → mybot references
- Updated workspace/*.md files with nanobot → mybot references
- Updated LICENSE copyright (kept "nanobot contributors" as attribution)

### Git Severance
- Deleted git tag `v0.1.3.post7`
- Removed `.git/` directory entirely to sever git connection

### Pre-existing Lint Issues
- 7 errors unrelated to channel removal (ExecToolConfig, CronService undefined, naming style issues)

---

## Discoveries

1. **Bridge directory** — Was only used for WhatsApp (using Baileys library), confirmed safe to delete entirely
2. **Docker files** — Were for deploying nanobot in Docker, not for nanobot to create containers
3. **Node.js requirement** — No longer needed after removing WhatsApp bridge; project is now pure Python
4. **Host dependencies** — Only Python 3.11+ is required
5. **Attribution** — LICENSE keeps "nanobot contributors" as attribution to original project

---

## Testing

Run tests with:
```bash
pytest
```

Lint with:
```bash
ruff check .
ruff format --check .
```

---

## License

MIT License (retained from nanobot)
