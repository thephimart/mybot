# Providers

mybot supports 18 LLM providers via LiteLLM.

## Provider Detection

Providers are detected automatically by:
1. Model name keywords (e.g., "claude" → Anthropic)
2. API key prefix (e.g., "sk-or-" → OpenRouter)
3. API base URL (e.g., "nvidia.com" → NVIDIA NIM)

Or explicitly set `agents.defaults.provider`.

## Available Providers

### Cloud Providers

| Provider | Key Prefix | Model Keywords | Env Variable |
|----------|------------|----------------|--------------|
| OpenAI | sk- | gpt-, o1- | OPENAI_API_KEY |
| Anthropic | sk-ant- | claude- | ANTHROPIC_API_KEY |
| DeepSeek | sk- | deepseek- | DEEPSEEK_API_KEY |
| Groq | gsk_ | llama-, mixtral- | GROQ_API_KEY |
| OpenRouter | sk-or- | any | OPENROUTER_API_KEY |
| Gemini | - | gemini- | GEMINI_API_KEY |
| Claude (via Azure) | - | azure/claude- | AZURE_API_KEY |

### Chinese Providers

| Provider | Env Variable | API Base |
|----------|--------------|----------|
| Zhipu (智谱) | ZHIPU_API_KEY | https://open.bigmodel.cn/api/paas/v4 |
| Dashscope (阿里云) | DASHSCOPE_API_KEY | https://dashscope.aliyuncs.com/api/v1 |
| Moonshot (月之暗面) | MOONSHOT_API_KEY | https://api.moonshot.cn/v1 |
| MiniMax | MINIMAX_API_KEY | https://api.minimax.chat/v1 |

### Local / Self-Hosted

| Provider | Default API Base | Description |
|----------|------------------|-------------|
| Ollama | http://localhost:11434 | Ollama local models |
| LM Studio | http://localhost:1234 | LM Studio |
| llama.cpp | http://localhost:8080 | llama.cpp server |
| vLLM | http://localhost:8000 | vLLM server |
| Custom | user-defined | Any OpenAI-compatible endpoint |

### Gateway / Proxy

| Provider | Key Prefix | API Base |
|----------|------------|----------|
| OpenRouter | sk-or- | https://openrouter.ai/api/v1 |
| AiHubMix | - | https://aihubmix.com/v1 |
| NVIDIA NIM | nvapi- | https://integrate.api.nvidia.com/v1 |
| OpenAI Codex | - | OAuth |

## Configuration

```json
{
  "agents": {
    "defaults": {
      "model": "openai/gpt-4o"
    }
  },
  "providers": {
    "openai": {
      "apiKey": "sk-..."
    }
  }
}
```

### Custom API Base

```json
{
  "providers": {
    "ollama": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:11434"
    }
  }
}
```

### Environment Variables

Providers also read from standard environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."
export OLLAMA_HOST="http://localhost:11434"
```

## Provider Selection

### Explicit Provider

```json
{
  "agents": {
    "defaults": {
      "model": "llama-3.1-70b",
      "provider": "ollama"
    }
  }
}
```

### Auto-Detection

Leave `provider` as null - mybot detects based on model name.

Examples:
- `anthropic/claude-sonnet-4-20250514` → Anthropic
- `gpt-4o` → OpenAI
- `deepseek-chat` → DeepSeek
- `meta-llama/Llama-3.1-70B-Instruct` → Auto-detect from key
