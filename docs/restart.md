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
