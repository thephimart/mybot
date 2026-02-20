# CLI Commands

## Main Commands

### mybot onboard

Initialize configuration and workspace.

```bash
mybot onboard
```

Creates `~/.mybot/config.json` and `~/.mybot/workspace/` with template files.

### mybot agent

Interact with agent directly.

```bash
# Send single message
mybot agent -m "Hello!"

# Interactive mode
mybot agent

# With image
mybot agent -i /path/to/image.jpg

# With audio
mybot agent -a /path/to/audio.mp3
```

Options:
- `-m, --message TEXT` - Message to send
- `-s, --session TEXT` - Session ID (default: cli:direct)
- `-i, --image PATH` - Image file path (can repeat)
- `-a, --audio PATH` - Audio file path (can repeat)
- `--markdown/--no-markdown` - Render markdown (default: true)
- `--logs/--no-logs` - Show runtime logs (default: false)

### mybot gateway

Start as persistent service with channels, cron, and heartbeat.

```bash
mybot gateway                    # Default port 18790
mybot gateway -p 8080            # Custom port
mybot gateway -v                 # Verbose output
```

### mybot status

Show current configuration status.

```bash
mybot status
```

---

## Channel Commands

### mybot channels status

Show channel status.

```bash
mybot channels status
```

---

## Cron Commands

### mybot cron list

List scheduled tasks.

```bash
mybot cron list
```

### mybot cron add

Add a scheduled task.

```bash
# Every 30 minutes
mybot cron add --every 30m "Check emails"

# Daily at 9am
mybot cron add --cron "0 9 * * *" "Morning summary"

# Once at specific time
mybot cron add --at "2026-01-01 12:00" "One-time task"
```

### mybot cron remove

Remove a scheduled task.

```bash
mybot cron remove <task-id>
```

### mybot cron enable

Enable or disable a task.

```bash
mybot cron enable <task-id> true
mybot cron enable <task-id> false
```

### mybot cron run

Run a task immediately.

```bash
mybot cron run <task-id>
```

---

## Provider Commands

### mybot provider login

OAuth login for providers (e.g., OpenAI Codex).

```bash
mybot provider login openai-codex
```
