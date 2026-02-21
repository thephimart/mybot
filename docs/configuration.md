# Configuration Reference

Full `config.json` schema.

## Location

`~/.mybot/config.json`

## Full Schema

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.mybot/workspace",
      "model": "anthropic/claude-opus-4-5",
      "provider": null,
      "max_tokens": 8192,
      "temperature": 0.7,
      "max_tool_iterations": 20,
      "memory_window": 50
    }
  },
  "channels": {
    "telegram": {
      "enabled": false,
      "token": "",
      "allow_from": [],
      "proxy": null
    },
    "email": {
      "enabled": false,
      "consent_granted": false,
      "imap_host": "",
      "imap_port": 993,
      "imap_username": "",
      "imap_password": "",
      "imap_mailbox": "INBOX",
      "imap_use_ssl": true,
      "smtp_host": "",
      "smtp_port": 587,
      "smtp_username": "",
      "smtp_password": "",
      "smtp_use_tls": true,
      "smtp_use_ssl": false,
      "from_address": "",
      "auto_reply_enabled": true,
      "poll_interval_seconds": 30,
      "mark_seen": true,
      "max_body_chars": 12000,
      "subject_prefix": "Re: ",
      "allow_from": []
    }
  },
  "providers": {
    "custom": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "anthropic": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "openai": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "openrouter": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "deepseek": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "groq": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "zhipu": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "dashscope": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "vllm": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "gemini": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "moonshot": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "minimax": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "aihubmix": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "openai_codex": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "nvidia_nim": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "ollama": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "lmstudio": { "apiKey": "", "apiBase": null, "extraHeaders": null },
    "llamacpp": { "apiKey": "", "apiBase": null, "extraHeaders": null }
  },
  "gateway": {
    "host": "0.0.0.0",
    "port": 18790
  },
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
  },
  "transcriber": {
    "use_local": true,
    "whisper_model": "base",
    "device": "cpu"
  }
}
```

## agents.defaults

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `workspace` | string | ~/.mybot/workspace | Working directory |
| `model` | string | anthropic/claude-opus-4-5 | LLM model |
| `provider` | string | auto-detect | Explicit provider |
| `max_tokens` | int | 8192 | Max response tokens |
| `temperature` | float | 0.7 | Sampling temperature |
| `max_tool_iterations` | int | 20 | Max tool calls per message |
| `memory_window` | int | 50 | Messages in context |

## channels.telegram

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | bool | false | Enable Telegram |
| `token` | string | - | Bot token from @BotFather |
| `allow_from` | array | [] | Allowed usernames/IDs |
| `proxy` | string | null | HTTP/SOCKS5 proxy URL |

## channels.email

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | bool | false | Enable Email |
| `consent_granted` | bool | false | Owner permission for mailbox |
| `imap_host` | string | - | IMAP server |
| `imap_port` | int | 993 | IMAP port |
| `imap_username` | string | - | IMAP username |
| `imap_password` | string | - | IMAP password |
| `smtp_host` | string | - | SMTP server |
| `smtp_port` | int | 587 | SMTP port |
| `auto_reply_enabled` | bool | true | Auto-reply to emails |
| `poll_interval_seconds` | int | 30 | Check interval |
| `max_body_chars` | int | 12000 | Max body length |

## providers

Each provider supports:
- `apiKey` - API key
- `apiBase` - Custom endpoint URL
- `extraHeaders` - Additional headers

See [Providers](providers.md) for details.

## tools

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `restrict_to_workspace` | bool | **true** | Restrict file/exec to workspace |
| `exec.timeout` | int | 300 | Shell command timeout (seconds) |
| `web.search.max_results` | int | 5 | Max web search results |

## transcriber

Speech-to-text (STT) transcription for voice messages.

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `use_local` | bool | true | true=faster-whisper (local), false=Groq API |
| `whisper_model` | string | base | Model size: tiny/base/small/medium/large-v3 |
| `device` | string | cpu | Device: cpu/cuda/auto (local only) |

**Providers:**
- `use_local: true` → faster-whisper (runs locally, no API key)
- `use_local: false` → Groq API (requires groq provider apiKey)

## tts

Text-to-speech (TTS) using local Kokoro. Generates audio files from text.

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | bool | false | Enable TTS tool |
| `voice` | string | af_heart | Voice preset |
| `lang_code` | string | b | Language code |

**Example:**
```json
{
  "tts": {
    "enabled": true,
    "voice": "af_heart",
    "lang_code": "b"
  }
}
```

**Usage:** Agent uses `speak` tool to generate audio, then `message` tool with `media` param to send.
