# Subagent Configuration

**Subagents are lightweight helper agents used for long-running, tool-heavy, or token-intensive tasks.**  
They allow the main agent to remain responsive and conserve context.

Configure subagent defaults in `agents.subagents`.  
When all values are `null`, subagents inherit from the main agent.

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

## Configuration Inheritance & Spawn Resolution

Agent configuration is resolved **at spawn time** and is **stateless**.

When a subagent is spawned, its configuration is constructed in the following order:

1. **Spawn-time arguments** (when used)
2. **Subagent configuration** from `config.json`
3. **Main agent defaults** from `config.json`

Later sources only apply when earlier values are unset (`null`).

Subagents do not persist configuration state.  
Any change to `config.json` affects the next spawned subagent automatically.

### Default Inheritance Behavior

If `agents.subagents` is empty or all values are `null`, subagents inherit the main agent’s defaults:

| Setting | Default |
|--------|---------|
| `model` | `anthropic/claude-opus-4-5` |
| `provider` | `null` (auto-detect) |
| `max_tokens` | `8192` |
| `temperature` | `0.7` |
| `max_tool_iterations` | `20` |

## Example: Different Model for Subagents

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "anthropic"
    },
    "subagents": {
      "model": "llama3.1",
      "provider": "ollama"
    }
  }
}
```
