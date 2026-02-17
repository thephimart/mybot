# Available Tools

This document describes the tools available to mybot.

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
exec(command: str, working_dir: str = None) -> str
```

**Safety Notes:**
- Commands have a configurable timeout (default 60s)
- Dangerous commands are blocked (rm -rf, format, dd, shutdown, etc.)
- Output is truncated at 10,000 characters
- Optional `restrictToWorkspace` config to limit paths

## Web Access

### web_search
Search the web using DDGS (DuckDuckGo).
```
web_search(query: str, count: int = 5, region: str = "us-en", safesearch: str = "moderate", timelimit: str | None = None) -> str
```
Returns search results with titles, URLs, and snippets. No API key required.

**Parameters:**
- `query` - Search query (required)
- `count` - Max results 1-10 (default 5)
- `region` - Region code: us-en, uk-en, ru-ru, etc. (default us-en)
- `safesearch` - on, moderate, off (default moderate)
- `timelimit` - d, w, m, y (optional)

### image_search
Search for images.
```
image_search(query: str, count: int = 5, region: str = "us-en", safesearch: str = "moderate", size: str | None = None, color: str | None = None, type_image: str | None = None) -> str
```
Returns image URLs, thumbnails, and sources.

**Parameters:**
- `query` - Image search query (required)
- `count` - Max results 1-10 (default 5)
- `region` - Region code (default us-en)
- `safesearch` - on, moderate, off (default moderate)
- `size` - Small, Medium, Large, Wallpaper (optional)
- `color` - Red, Orange, Yellow, Green, Blue, etc. (optional)
- `type_image` - photo, clipart, gif, transparent, line (optional)

### video_search
Search for videos.
```
video_search(query: str, count: int = 5, region: str = "us-en", safesearch: str = "moderate", timelimit: str | None = None, resolution: str | None = None, duration: str | None = None) -> str
```
Returns video URLs, descriptions, and duration.

**Parameters:**
- `query` - Video search query (required)
- `count` - Max results 1-10 (default 5)
- `region` - Region code (default us-en)
- `safesearch` - on, moderate, off (default moderate)
- `timelimit` - d, w, m (optional)
- `resolution` - high, standard (optional)
- `duration` - short, medium, long (optional)

### news_search
Search for news articles.
```
news_search(query: str, count: int = 5, region: str = "us-en", safesearch: str = "moderate", timelimit: str | None = None) -> str
```
Returns news titles, URLs, sources, and dates.

**Parameters:**
- `query` - News search query (required)
- `count` - Max results 1-10 (default 5)
- `region` - Region code (default us-en)
- `safesearch` - on, moderate, off (default moderate)
- `timelimit` - d, w, m (optional)

### books_search
Search for books.
```
books_search(query: str, count: int = 5) -> str
```
Returns book titles, authors, publishers, and download links.

**Parameters:**
- `query` - Book search query (required)
- `count` - Max results 1-10 (default 5)

### web_fetch
Fetch and extract main content from a URL.
```
web_fetch(url: str, extractMode: str = "markdown", maxChars: int = 50000) -> str
```

**Notes:**
- Content is extracted using readability
- Supports markdown or plain text extraction
- Output is truncated at 50,000 characters by default

## Communication

### message
Send a message to the user (used internally).
```
message(content: str, channel: str = None, chat_id: str = None) -> str
```

## Background Tasks

### spawn
Spawn a subagent to handle a task in the background.
```
spawn(task: str, label: str = None) -> str
```

Use for complex or time-consuming tasks that can run independently. The subagent will complete the task and report back when done.

## Scheduled Reminders (Cron)

Use the `exec` tool to create scheduled reminders with `mybot cron add`:

### Set a recurring reminder
```bash
# Every day at 9am
mybot cron add --name "morning" --message "Good morning! ☀️" --cron "0 9 * * *"

# Every 2 hours
mybot cron add --name "water" --message "Drink water! 💧" --every 7200
```

### Set a one-time reminder
```bash
# At a specific time (ISO format)
mybot cron add --name "meeting" --message "Meeting starts now!" --at "2025-01-31T15:00:00"
```

### Manage reminders
```bash
mybot cron list              # List all jobs
mybot cron remove <job_id>   # Remove a job
```

## Heartbeat Task Management

The `HEARTBEAT.md` file in the workspace is checked every 30 minutes.
Use file operations to manage periodic tasks:

### Add a heartbeat task
```python
# Append a new task
edit_file(
    path="HEARTBEAT.md",
    old_text="## Example Tasks",
    new_text="- [ ] New periodic task here\n\n## Example Tasks"
)
```

### Remove a heartbeat task
```python
# Remove a specific task
edit_file(
    path="HEARTBEAT.md",
    old_text="- [ ] Task to remove\n",
    new_text=""
)
```

### Rewrite all tasks
```python
# Replace the entire file
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
