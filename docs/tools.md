# Tools

Tools extend the agent's capabilities to interact with the world.

## Configuration

```json
{
  "tools": {
    "web": {
      "search": {
        "max_results": 5
      }
    },
    "exec": {
      "timeout": 300
    },
    "restrict_to_workspace": true,
    "mcp_servers": {}
  }
}
```

## restrict_to_workspace

When `true`, restricts all file and shell operations to the workspace directory.

| Value | Effect |
|-------|--------|
| `true` | Only access `~/.mybot/workspace/*` |
| `false` | Full filesystem access (default: true) |

**Warning:** Default changed to `true` for security. Set to `false` only if you need broader access.

## exec.timeout

Shell command timeout in seconds. Default: 300 (5 minutes).

## Web Tools

### web_search

Search the web using DuckDuckGo.

Parameters:
- `query` (required) - Search query
- `count` - Max results (1-10)
- `region` - Region (us-en, uk-en, etc.)
- `safesearch` - on/moderate/off
- `timelimit` - d/w/m/y

### web_fetch

Fetch and extract content from URLs.

Parameters:
- `url` (required) - URL to fetch
- `extractMode` - markdown/text
- `maxChars` - Max characters

## File Tools

### read_file

Read file contents.

### write_file

Create or overwrite files.

### edit_file

Edit file contents (find/replace).

### list_dir

List directory contents.

## Audio Tools

### speak

Generate speech from text using local Kokoro TTS. Requires `tts.enabled: true` in config.

Parameters:
- `text` (required) - Text to synthesize
- `voice` - Voice preset (default: af_heart)
- `lang_code` - Language code (default: b)

Returns: File path to generated WAV audio.

**Usage:**
```python
# Generate speech
path = speak(text="Hello world")

# Send as voice message
message(content="Here's your message", media=[path])
```

### transcribe_audio

Transcribe audio files to text.

Parameters:
- `path` (required) - Path to audio file
- `language` - Language code (optional)

Supports: .ogg, .wav, .mp3

**Note:** Inbound voice messages are automatically transcribed. This tool is for agent-initiated transcription of audio files.

---

## MCP Servers

Connect to MCP (Model Context Protocol) servers:

```json
{
  "tools": {
    "mcp_servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
      }
    }
  }
}
```

Or HTTP:

```json
{
  "tools": {
    "mcp_servers": {
      "my-server": {
        "url": "http://localhost:3000"
      }
    }
  }
}
```
