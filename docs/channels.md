# Channels

Channels allow mybot to receive and send messages via different protocols.

## Overview

mybot supports two channels:
- **Telegram** - Bot messages
- **Email** - IMAP/SMTP

Channels are enabled in `config.json` and only active when running `mybot gateway`.

## Telegram

### Setup

1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Get the bot token
3. Configure in `config.json`:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      "allow_from": ["username1", "username2"],
      "proxy": null
    }
  }
}
```

### Configuration

| Setting | Description |
|---------|-------------|
| `enabled` | Set to true to enable |
| `token` | Bot token from @BotFather |
| `allow_from` | Array of allowed usernames/IDs. Empty = anyone |
| `proxy` | Optional HTTP/SOCKS5 proxy (e.g., `http://127.0.0.1:7890`) |

### Commands

The bot responds to:
- `/start` - Start conversation
- `/new` - Start new session
- `/help` - Show help

### Images and Photos

Telegram supports sending images and photos to the bot. Any vision-enabled model
(e.g., GPT-4o, Claude 4, Gemini) can analyze these images.

### Voice Messages (STT)

Voice messages are automatically transcribed using the configured transcriber
(see [Configuration](configuration.md#transcriber)). Supports:
- **Local**: faster-whisper (no API key required)
- **Cloud**: Groq API (requires API key in groq provider config)

### Running

```bash
mybot gateway
```

The bot will respond to messages from allowed users.

---

## Email

### Setup

Configure IMAP (receive) and SMTP (send) in `config.json`:

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consent_granted": true,
      "imap_host": "imap.gmail.com",
      "imap_port": 993,
      "imap_username": "your-email@gmail.com",
      "imap_password": "app-password",
      "imap_mailbox": "INBOX",
      "smtp_host": "smtp.gmail.com",
      "smtp_port": 587,
      "smtp_username": "your-email@gmail.com",
      "smtp_password": "app-password",
      "smtp_use_tls": true,
      "from_address": "Your Name <your-email@gmail.com>",
      "auto_reply_enabled": true,
      "poll_interval_seconds": 30,
      "allow_from": []
    }
  }
}
```

### Gmail Note

For Gmail, you need an "App Password":
1. Enable 2-Factor Authentication
2. Go to Google Account → Security
3. App passwords → Generate new password

### Configuration

| Setting | Description |
|---------|-------------|
| `enabled` | Set to true to enable |
| `consent_granted` | Must be true to process emails |
| `imap_host` | IMAP server (e.g., imap.gmail.com) |
| `imap_username` | IMAP username |
| `imap_password` | IMAP password or app password |
| `smtp_host` | SMTP server |
| `smtp_username` | SMTP username |
| `smtp_password` | SMTP password |
| `auto_reply_enabled` | Auto-reply to inbound emails |
| `poll_interval_seconds` | How often to check for new emails |
| `allow_from` | Only process emails from these senders |

### Running

```bash
mybot gateway
```

The bot will check for new emails and auto-reply.
