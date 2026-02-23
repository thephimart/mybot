# Subagent Configuration

Configure subagent defaults in `agents.subagents`. When all values are `null`, subagents inherit from the main agent.

## Settings

```json
{
  "agents": {
    "subagents": {
      "model": null,
      "provider": null,
      "max_tokens": null,
      "temperature": null,
      "max_tool_iterations": null
    }
  }
}
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `model` | string | inherit | LLM model, null = inherit from main agent |
| `provider` | string | inherit | LLM provider, null = inherit from main agent |
| `max_tokens` | int | inherit | Max tokens, null = inherit (8192) |
| `temperature` | float | inherit | Randomness, null = inherit (0.7) |
| `max_tool_iterations` | int | inherit | Max tool calls, null = inherit (20) |

## Inheritance

When `agents.subagents` is empty or all values are `null`, subagents use the main agent's settings:

| Setting | Main Agent Default |
|---------|-------------------|
| model | anthropic/claude-opus-4-5 |
| provider | null (auto-detect) |
| max_tokens | 8192 |
| temperature | 0.7 |
| max_tool_iterations | 20 |

## Example: Different Model for Subagents

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    },
    "subagents": {
      "model": "llama3.1",
      "provider": "ollama"
    }
  }
}
```

## Override at Spawn Time

Pass parameters directly to the spawn tool:

```
spawn(task="analyze this", model="qwen2.5", provider="ollama", api_base="http://localhost:8080/v1")
```

Available overrides: `model`, `provider`, `api_base`, `api_key`

See [Workspace](workspace.md) for memory files.
