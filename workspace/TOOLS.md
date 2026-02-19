# Available Tools

This document describes the tools available to mybot. All tools listed here are available **unless** explicitly stated otherwise in skill metadata.

**Note:** The agent has access to these tools directly via function calling. Do NOT use CLI commands as a workaround when a native tool exists.

## Tool Availability by Mode

| Tool | `mybot agent` (direct) | `mybot gateway` (service) |
|------|-------------------------|--------------------------|
| read_file, write_file, edit_file, list_dir | ✅ | ✅ |
| exec | ✅ | ✅ |
| web_search, web_fetch | ✅ | ✅ |
| spawn | ✅ | ✅ |
| message | ⚠️ requires context | ✅ |
| cron | ❌ CLI only | ✅ |
| mcp_* | ✅ (if configured) | ✅ (if configured) |

**Note:** The `cron` tool is only available in gateway mode. Use CLI commands (`mybot cron add ...`) in agent mode.

## File Operations

### read_file
Read the contents of a file.
```
read_file(path: str) -> str
```

### write_file
Write content to a file (creates parent directories if needed).
```
write_file(path: str, content: str) -> str
```

### edit_file
Edit a file by replacing the specific instance of text.
```
edit_file(path: str, old_text: str, new_text: str) -> str
```

### list_dir
List contents of a directory.
```
list_dir(path: str) -> str
```

## Shell Execution

### exec
Execute a shell command and return output.
```
exec(command: str, working_dir: str = null) -> str
```

**Safety Notes:**
- Commands have a configurable timeout (default 300s)
- Dangerous commands are blocked (rm -rf, format, dd, shutdown, etc.)
- Output is truncated at 10,000 characters
- Optional `restrictToWorkspace` config to limit paths

## Web Access

All web tools use the `ddgs` Python library (DuckDuckGo) and require no API key.

### web_search
Search the web for text results.
```
web_search(query: str, count: int = 5, region: str = "us-en", safesearch: str = "moderate", timelimit: str | null = null) -> str
```

Returns titles, URLs, and snippets.

### web_fetch
Fetch and extract main content from a URL.
```
web_fetch(url: str, extractMode: str = "markdown", maxChars: int = 50000) -> str
```

Uses readability for HTML extraction. Returns JSON with extracted text, status, and metadata.

## Communication

### message
Send a message to the user on a chat channel.
```
message(content: str, channel: str = null, chat_id: str = null) -> str
```

Requires both channel and chat_id. In gateway mode these are set automatically from the incoming message context. In chat mode, you must specify them explicitly.

## Background Tasks

### spawn
Spawn a subagent to handle a task in the background.
```
spawn(task: str, label: str = null) -> str
```

The subagent will complete the task and report back when done.

## Scheduling

### cron (CLI)

Use the CLI to schedule reminders. Available commands:

```
mybot cron add --name "reminder" --message "TEXT" --cron "0 9 * * *"
mybot cron add --name "reminder" --message "TEXT" --every 7200
mybot cron add --name "reminder" --message "TEXT" --at "2026-02-12T10:30:00"
mybot cron list
mybot cron remove <job_id>
```

- `--cron` - cron expression (e.g., "0 9 * * *" for daily at 9am)
- `--every` - interval in seconds (e.g., 7200 for every 2 hours)
- `--at` - one-time execution (ISO format)

## MCP Servers

MCP (Model Context Protocol) servers can be configured to expose additional tools. When configured, MCP tools are automatically loaded and available with the `mcp_` prefix (e.g., `mcp_servername_toolname`).

## Heartbeat Tasks

The `HEARTBEAT.md` file in the workspace is checked every 30 minutes for high-priority tasks.

**Note:** Heartbeat is only active in gateway mode (`mybot gateway`), not in chat mode.

To manage heartbeat tasks, use file operations:

### Add a heartbeat task
```
edit_file(
    path="HEARTBEAT.md",
    old_text="## Example Tasks",
    new_text="- [ ] New periodic task here\n\n## Example Tasks"
)
```

### Remove a heartbeat task
```
edit_file(
    path="HEARTBEAT.md",
    old_text="- [ ] Task to remove\n",
    new_text=""
)
```

### Rewrite all tasks
```
write_file(
    path="HEARTBEAT.md",
    content="# Heartbeat Tasks\n\n- [ ] Task 1\n- [ ] Task 2\n"
)
```

---

## Adding Custom Tools

To add custom tools:
1. Create a class that extends `Tool` in `mybot/agent/tools/`
2. Implement `name`, `description`, `parameters`, and `execute`
3. Register it in `AgentLoop._register_default_tools()`
