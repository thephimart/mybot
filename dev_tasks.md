# mybot Development Tasks

---

## Pending

### RestartTool Implementation

**Goal:** Add gateway restart capability via systemd supervision.

**Philosophy:** External supervision required — mybot does not supervise itself.

#### Implementation Plan

##### 1. New File: `mybot/agent/tools/restart.py`

```python
"""Restart tool for gateway restart requests."""

import asyncio
from typing import Any

from mybot.agent.tools.base import Tool


class RestartTool(Tool):
    """Tool to request gateway restart via systemd."""

    def __init__(self, service_name: str = "mybot"):
        self._service_name = service_name

    @property
    def name(self) -> str:
        return "restart"

    @property
    def description(self) -> str:
        return f"Request gateway restart via {self._service_name}. Requires systemd."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        try:
            process = await asyncio.create_subprocess_exec(
                "systemctl", "restart", self._service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15)

            if process.returncode == 0:
                return f"Restart requested for {self._service_name}. Gateway will restart."
            else:
                err = stderr.decode() if stderr else "unknown error"
                return f"Failed to restart: {err}"
        except asyncio.TimeoutError:
            return "Restart command timed out"
        except FileNotFoundError:
            return "systemd not found. External supervision required."
        except Exception as e:
            return f"Error: {str(e)}"
```

##### 2. Modify: `mybot/agent/loop.py`

- Add import (line ~20):
  ```python
  from mybot.agent.tools.restart import RestartTool
  ```

- Register in `_register_default_tools()` (after cron tool, ~line 136):
  ```python
  # Restart tool
  self.tools.register(RestartTool())
  ```

##### 3. New File: `docs/restart.md`

```markdown
# Gateway Restart

**mybot does not supervise itself.**

The agent may request a restart, but the system decides.

## RestartTool

The `restart` tool requests systemd to restart the gateway:

```
restart()
```

Returns success if systemd processed the request.

⚠️ **Security note**

The restart tool executes a privileged system command (`systemctl restart mybot`).
Only enable it in trusted deployments.

If you don't want restart capability, simply delete `mybot/agent/tools/restart.py`.

## Requirements

1. **mybot must run as a systemd service**
2. **Service name must be `mybot`** (or configured in RestartTool)

## Setup: systemd service

Create `/etc/systemd/system/mybot.service`:

```ini
[Unit]
Description=mybot AI assistant
After=network.target

[Service]
Type=simple
User=phil
WorkingDirectory=/home/phil/opencode/mybot
ExecStart=/home/phil/.local/bin/mybot gateway
Restart=always
RestartSec=10
Environment=PATH=/home/phil/.local/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mybot
```

## Viewing logs

```bash
journalctl -u mybot -f
```

## Why external supervision?

- PID tracking ✓
- Crash recovery ✓
- Restart rate limiting ✓
- Log management ✓
- Survives kernel hiccups ✓

RestartTool is inert without systemd. The agent can request; systemd decides.

---

**No restart tool? No problem.**

Run `mybot gateway` directly — just manually restart when needed.
```

##### 4. Modify: `docs/index.md`

Add to navigation section:
```markdown
- [Gateway Restart](restart.md)
```

#### File Summary

| File | Action |
|------|--------|
| `mybot/agent/tools/restart.py` | Create |
| `mybot/agent/loop.py` | Add import + 1 line registration |
| `docs/restart.md` | Create |
| `docs/index.md` | Add link |

#### Recommended Release Note

```
0.4.1

Add optional restart tool for systemd-managed deployments

- Enables agent-requested gateway restarts under external supervision
- Inert by default; no behavior change without systemd
```

That wording reassures people immediately.

#### Security Properties

| Property | How It's Enforced |
|----------|-------------------|
| No parameter abuse | `parameters: {}` — no user input accepted |
| No shell injection | `create_subprocess_exec` — no shell interpretation |
| No command flexibility | Hardcoded `systemctl restart <service>` |
| Fails gracefully | Returns helpful error if systemd missing |
| Deletion-friendly | Single file, registered in one place |

---

## Testing / Bug Hunting

Active investigation for issues in the codebase.

---

## Unclosed Client Session (Telegram)

Gateway shows "Unclosed client session" warnings on shutdown.

**Root cause:** python-telegram-bot's `HTTPXRequest` doesn't close underlying httpx client.

**Fix:** Call `HTTPXRequest.close()` after app shutdown in `telegram.py:stop()`.

---

## Future

### Kokoro TTS Integration

Research local TTS with kokoro package. See https://pypi.org/project/kokoro/

---

### Stable Diffusion CPP Integration

Research local image generation. See https://pypi.org/project/stable-diffusion-cpp-python/

---

## Completed

(All completed tasks moved to git history)
