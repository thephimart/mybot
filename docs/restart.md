# Gateway Restart

**mybot does not supervise itself.**

The agent may request a restart, but the system decides.

## RestartTool

The `restart` tool requests systemd to restart the gateway:

```
restart()
```

Returns success if systemd processed the request.

The restart tool executes:
```
systemctl --user restart mybot
```

This works when mybot is installed as a systemd *user service* with lingering enabled.

⚠️ **Security note**

RestartTool does not require sudo and cannot manage arbitrary system services.
It is limited to the user's own systemd service.

This is the recommended and safest deployment model.

If you don't want restart capability, simply delete `mybot/agent/tools/restart.py`.

## One-time setup: enable lingering

To allow mybot to start at boot and restart itself without sudo, enable lingering
for the user account running mybot.

This command is required once:

```bash
sudo loginctl enable-linger <user>
```

After this:
- User services start at boot and persist across reboots
- No further sudo access is required
- RestartTool can restart the gateway remotely

## Requirements

- mybot runs as a systemd *user service*
- Lingering is enabled for the user (one-time sudo step)
- Service name matches RestartTool configuration

## Setup: systemd user service

Create the user service file:

```
~/.config/systemd/user/mybot.service
```

```ini
[Unit]
Description=mybot AI assistant
After=network.target

[Service]
Type=simple
WorkingDirectory=<absolute-path-to-mybot>
ExecStart=<absolute-path-to-mybot>/.venv/bin/mybot gateway
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

⚠️ Do not include `User=` in user services

- `<absolute-path-to-mybot>` — replace with the absolute path to your mybot folder (e.g., `/home/user/mybot`). This example assumes you installed mybot in a `.venv` within the mybot folder. If you installed elsewhere, adjust the path to your mybot binary accordingly.

Then:
```bash
systemctl --user daemon-reload
systemctl --user enable --now mybot
```

## Viewing logs

```bash
journalctl --user -u mybot -f
```

## Why external supervision?

- PID tracking ✓
- Crash recovery ✓
- Restart rate limiting ✓
- Log management ✓
- Survives kernel hiccups ✓

RestartTool requires a systemd user service to function.

---

**No restart tool? No problem.**

Run `mybot gateway` directly — just manually restart when needed.
