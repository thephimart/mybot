# Subagents

Subagents are background tasks spawned by the main agent to handle complex or time-consuming work independently. They complete their task and report back when done.

## When to Use Subagents

- Long-running operations that would block the main agent
- Parallel independent tasks
- Background research or file processing
- Any task that doesn't need immediate user feedback

## How Subagents Work

The main agent uses the `spawn` tool to create a subagent:

```
spawn(task="search for...", label="research")
```

The subagent:
1. Runs independently in the background
2. Has its own conversation context
3. Uses tools just like the main agent
4. Reports back when complete

## Configuration

### Default Behavior (All Null)

When all `agents.subagents` values are `null` (or not set), subagents **inherit from the main agent**:

| Setting | Subagent Inherits From |
|---------|----------------------|
| `model` | Main agent's model |
| `provider` | Main agent's provider |
| `max_tokens` | Main agent's max_tokens (8192) |
| `temperature` | Main agent's temperature (0.7) |
| `max_tool_iterations` | Main agent's max_tool_iterations (20) |

### Setting Subagent Defaults

To give subagents their own defaults, configure `agents.subagents` in config.json:

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    },
    "subagents": {
      "model": "meta/llama-3.1-70b-instruct",
      "provider": "ollama",
      "max_tool_iterations": 10
    }
  }
}
```

### Override at Spawn Time

You can override settings per-task when spawning:

```
spawn(task="analyze this file", model="llama3.1", provider="ollama")
```

Available overrides:
- `model` — LLM model (e.g., 'llama3.1')
- `provider` — LLM provider (e.g., 'ollama', 'llamacpp')
- `api_base` — API base URL (e.g., 'http://localhost:11434/v1')
- `api_key` — API key override

## Setting Resolution Order

Settings are resolved in this priority order:

1. **Explicit spawn parameters** — Values passed directly to `spawn()` call
2. **Subagents config** — `agents.subagents` in config.json
3. **Main agent defaults** — `agents.defaults` in config.json
4. **Hardcoded defaults** — Model/temperature/max_tokens built-in values

For example, a subagent's model is resolved as:
```
spawn.model → config.agents.subagents.model → config.agents.defaults.model → provider default
```

## Provider Resolution

Subagents use LiteLLM to support multiple providers. The provider is resolved as:

1. Explicit `provider` param in spawn call
2. `agents.subagents.provider` in config.json
3. Auto-detected from model name (if model is an OpenAI-compatible model string)

If using a local provider (ollama, llamacpp, etc.) without explicit api_base:
- Checks `agents.subagents` for api_base
- Falls back to `providers.<provider>.apiBase`
- Raises error if api_base is required but not found

## Example Configurations

### Minimal (Inherit Everything)

```json
{
  "agents": {}
}
```

Subagents use the same model and provider as the main agent.

### Subagent with Different Model

```json
{
  "agents": {
    "subagents": {
      "model": "meta/llama-3.1-70b-instruct",
      "provider": "ollama"
    }
  },
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434"
    }
  }
}
```

### Per-Task Override

No config change needed — just pass parameters to spawn:

```
spawn(task="run this analysis", model="qwen2.5-coder", api_base="http://localhost:8080/v1")
```

## Tools Available to Subagents

Subagents have most tools available to the main agent:
- File tools (read, write, edit, list)
- Shell execution
- Web tools (fetch, search)
- TTS (if configured)

Subagents **cannot**:
- Spawn other subagents (no spawn tool)
- Send messages to channels (no message tool)

## Deletion

If you don't want subagent capability, simply delete `mybot/agent/tools/spawn.py`.
