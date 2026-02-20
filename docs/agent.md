# Agent Configuration

Configure the agent behavior in `agents.defaults`.

## Settings

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
  }
}
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `workspace` | string | ~/.mybot/workspace | Working directory for files, memory, skills |
| `model` | string | anthropic/claude-opus-4-5 | LLM model name |
| `provider` | string | null | Explicit provider, null = auto-detect |
| `max_tokens` | int | 8192 | Maximum tokens in response |
| `temperature` | float | 0.7 | Randomness (0=deterministic, 2=creative) |
| `max_tool_iterations` | int | 20 | Max tool calls per message |
| `memory_window` | int | 50 | Messages to keep in context |

## Model Selection

### Cloud Models

```json
{
  "model": "openai/gpt-4o"
}
{
  "model": "anthropic/claude-sonnet-4-20250514"
}
{
  "model": "deepseek-chat"
}
```

### Local Models

```json
{
  "model": "llama-3.1-70b-instruct",
  "provider": "ollama"
}
```

## Temperature

| Value | Effect |
|-------|--------|
| 0.0 - 0.3 | Focused, deterministic |
| 0.4 - 0.7 | Balanced |
| 0.8 - 1.0 | Creative, unpredictable |

## Memory Window

The agent maintains conversation history. Higher values = more context but more tokens.

- 10 - Short conversations
- 50 - Default, good balance
- 100 - Long conversations

See [Workspace](workspace.md) for memory files.
