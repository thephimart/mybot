# Quick Start

## 1. Initialize Configuration

```bash
mybot onboard
```

This creates:
- `~/.mybot/config.json` - Configuration file
- `~/.mybot/workspace/` - Workspace directory with templates

## 2. Configure API Key

Edit `~/.mybot/config.json`:

```json
{
  "agents": {
    "defaults": {
      "model": "openai/gpt-4o"
    }
  },
  "providers": {
    "openai": {
      "apiKey": "sk-your-key-here"
    }
  }
}
```

See [Providers](providers.md) for all available providers.

## 3. Test with CLI

```bash
mybot agent -m "Hello!"
```

Or interactive mode:
```bash
mybot agent
```

## 4. Run as Service (Optional)

To receive Telegram messages:

```bash
mybot gateway
```

See [Channels](channels.md) to enable Telegram or Email.

## Next Steps

- [Configuration](configuration.md) - Full config reference
- [Workspace Files](workspace.md) - Customize agent behavior
- [CLI Commands](cli.md) - All available commands
