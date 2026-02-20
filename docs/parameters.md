# LiteLLM Parameters Reference

This document lists all available parameters that can be passed through LiteLLM when calling LLM providers. Parameters are organized into three sections: Global, Provider-Specific, and Model-Specific.

---

## Table of Contents

1. [Global Parameters](#global-parameters)
2. [Provider-Specific Parameters](#provider-specific-parameters)
3. [Model-Specific Notes](#model-specific-notes)
4. [Configuration File Parameters](#configuration-file-parameters)

---

## Global Parameters

These parameters work with most OpenAI-compatible providers (OpenAI, NVIDIA NIM, OpenRouter, DeepSeek, Azure, etc.).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | float | 0.7 | Controls randomness. Range: 0-2. Higher values (e.g., 0.8) produce more diverse/creative outputs. Lower values (e.g., 0.2) produce more focused/deterministic outputs. |
| `top_p` | float | 1.0 | Nucleus sampling - alternative to temperature. Controls the cumulative probability of token selection. Lower values restrict to more likely tokens. Should not be used with temperature. |
| `max_tokens` | int | varies | Maximum number of tokens to generate in the response. Some models have different limits. |
| `max_completion_tokens` | int | varies | Alternative to max_tokens. Specifies only the maximum tokens for the completion, separate from prompt tokens. Some models prefer this over max_tokens. |
| `n` | int | 1 | Number of chat completion choices to generate for each input message. Creates multiple independent responses. |
| `stream` | bool | false | If true, sends partial message deltas (tokens) as they become available, instead of waiting for the complete response. |
| `stop` | str or list | null | Up to 4 sequences where the API will stop generating further tokens. Can be a single string or list of strings. |
| `presence_penalty` | float | 0 | Range: -2.0 to 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. |
| `frequency_penalty` | float | 0 | Range: -2.0 to 2.0. Positive values penalize new tokens based on their frequency in the text so far, decreasing the model's likelihood to repeat the same words. |
| `logit_bias` | dict | null | Modify the likelihood of specific tokens appearing in the completion. Maps token IDs (integers) to bias values (-100 to 100). |
| `logprobs` | bool | false | Whether to return log probabilities of the output tokens. If true, returns the logprobs for the most likely tokens. |
| `top_logprobs` | int | null | Number of most likely tokens (0-20) to return log probabilities for. Requires logprobs to be true. |
| `seed` | int | null | If specified, the model will make a best effort to sample deterministically (same seeds = same outputs). Not guaranteed to be deterministic. |
| `user` | string | null | A unique identifier representing your end-user. Helps the API to monitor and detect abuse. |
| `tools` | list | null | A list of tools (functions) the model may call. Each tool has name, description, and parameters defined as JSON Schema. |
| `tool_choice` | string/dict | "auto" | Controls which tool is called. Values: "auto" (model decides), "none" (no tool), or specify a tool by name. |
| `parallel_tool_calls` | bool | true | Whether to allow the model to call multiple tools in parallel. |
| `response_format` | dict | null | Specifies the format the model must output. Use for JSON mode or Structured Outputs. Provide a JSON Schema object. |
| `modalities` | list | null | Specifies modalitites for vision/audio. Values: `["text"]`, `["text", "image"]`, `["text", "audio"]`. Not supported by all providers (e.g., NVIDIA NIM). |
| `thinking` | dict | null | Enable extended thinking/reasoning for supported models. Anthropic: `{"type": "enabled", "budget_tokens": 1024}` or `{"type": "disabled"}`. |
| `reasoning_effort` | string | null | Control reasoning effort for reasoning models. Values: "none", "low", "medium", "high". Supported by DeepSeek, Anthropic, Mistral, Groq, etc. |
| `stream_options` | dict | null | Options for streaming responses. Set `{"include_usage": true}` to include usage data in streaming chunks. |
| `prediction` | dict | null | Provide a predicted output to accelerate generation. Contains `type` and `content` keys. |
| `extra_headers` | dict | null | Additional HTTP headers to pass with the request. Useful for provider-specific auth (e.g., APP-Code for AiHubMix). |
| `max_retries` | int | 0 | Number of times to retry the request if it fails. LiteLLM handles retries automatically if configured. |
| `prompt_cache_key` | string | null | Key for prompt caching. Used with providers that support prompt caching. |
| `service_tier` | string | null | Service tier for the request. Some providers offer different service levels. |
| `audio` | dict | null | Audio input configuration for models that support audio input. |
| `web_search_options` | dict | null | Options for web search capabilities. Provider-specific. |
| `safety_identifier` | string | null | Identifier for safety/filtering settings. Provider-specific. |

---

## Provider-Specific Parameters

These parameters are specific to certain providers and may not work with all providers.

### Anthropic (Claude)

| Parameter | Type | Description |
|-----------|------|-------------|
| `thinking` | dict | Enable extended thinking. Values: `{"type": "enabled", "budget_tokens": 1024}` or `{"type": "disabled"}`. Budget tokens controls how many tokens can be used for thinking (1024-8000). |
| `thinking_budget_tokens` | int | Maximum tokens allocated for thinking/reasoning. Must be used with thinking={"type": "enabled"}. |
| `speed` | string | Response speed. Values: "fast" (faster, less thorough) or "balanced" (default). |
| `reasoning_effort` | string | Control reasoning. Values: "none", "low", "medium", "high". |
| `metadata` | dict | User identification metadata. Example: `{"user_id": "user123"}`. |

### AWS Bedrock

| Parameter | Type | Description |
|-----------|------|-------------|
| `aws_region_name` | string | AWS region for the request (e.g., "us-east-1"). |
| `aws_role_name` | string | IAM role to assume for the request. |
| `request_metadata` | dict | Metadata for cost attribution and logging. Example: `{"cost_center": "engineering"}`. |

### Google/Gemini

| Parameter | Type | Description |
|-----------|------|-------------|
| `generation_config` | dict | Generation configuration dict with temperature, top_p, top_k, etc. |
| `safety_settings` | dict | Safety settings for content filtering. |
| `system_instruction` | string | System instruction for the model. |
| `labels` | dict | Resource labeling for Vertex AI. Example: `{"environment": "production"}`. |

### Azure OpenAI

| Parameter | Type | Description |
|-----------|------|-------------|
| `azure_ad_token` | string | Azure Active Directory token for authentication. |
| `api_version` | string | Azure API version (e.g., "2024-02-15-preview"). |
| `deployment_id` | string | Azure deployment ID for the model. |

### Ollama

| Parameter | Type | Description |
|-----------|------|-------------|
| `format` | string | Force output format. Values: "json" for JSON mode, "xml", etc. |
| `options` | dict | Model-specific options (temperature, top_p, etc.) passed directly to Ollama. |
| `num_predict` | int | Equivalent to max_tokens for Ollama. |
| `temperature` | float | Model-specific temperature (overrides global). |
| `top_p` | float | Model-specific top_p (overrides global). |

### vLLM (Local Deployment)

| Parameter | Type | Description |
|-----------|------|-------------|
| `gpu_memory_utilization` | float | GPU memory utilization (0.0-1.0). Percentage of GPU memory to use. |
| `tensor_parallel_size` | int | Tensor parallelism degree for multi-GPU setups. |
| `max_num_seqs` | int | Maximum number of sequences per request. |
| `disable_log_requests` | bool | Disable logging of individual requests. |

### Cohere

| Parameter | Type | Description |
|-----------|------|-------------|
| `preamble` | string | Preamble prompt that prepends the conversation. |
| `search_options` | dict | Options for search-augmented generation. |
| `documents` | list | Documents for retrieval-augmented generation. |

### HuggingFace

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_new_tokens` | int | Maximum new tokens to generate. |
| `temperature` | float | Sampling temperature. |
| `top_p` | float | Nucleus sampling probability. |
| `top_k` | int | Top-k sampling parameter. |
| `repetition_penalty` | float | Repetition penalty. |

### TogetherAI

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_tokens_to_sample` | int | Maximum tokens to generate (equivalent to max_tokens). |
| `temperature` | float | Sampling temperature. |
| `top_p` | float | Nucleus sampling. |
| `top_k` | int | Top-k sampling. |

### Replicate

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_new_tokens` | int | Maximum new tokens to generate. |
| `temperature` | float | Sampling temperature. |
| `top_p` | float | Nucleus sampling. |
| `webhook` | string | Webhook URL for async completion. |

### Petals

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_new_tokens` | int | Maximum new tokens to generate. |
| `temperature` | float | Sampling temperature. |
| `top_p` | float | Nucleus sampling. |

### Palm/PaLM (Google)

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxOutputTokens` | int | Maximum output tokens. |
| `temperature` | float | Sampling temperature. |
| `top_p` | float | Nucleus sampling. |
| `top_k` | int | Top-k sampling. |

### AI21 Labs

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxOutputTokens` | int | Maximum output tokens. |
| `temperature` | float | Sampling temperature. |
| `top_p` | float | Nucleus sampling. |

---

## Model-Specific Notes

### Reasoning Models

Models like DeepSeek R1, Claude with thinking enabled, and similar require special handling:

- **DeepSeek R1**: Use `reasoning_effort` parameter ("none", "low", "medium", "high")
- **Claude (Anthropic)**: Use `thinking` parameter to enable extended thinking
- **Switching models**: When switching between reasoning and non-reasoning models, set `drop_params=True` to avoid errors with unsupported parameters

### Vision Models

- Vision models support the `modalities` parameter to specify input types
- Format images as `{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}`
- **Note**: Some providers (like NVIDIA NIM) do not support the `modalities` parameter - images work without it

### Audio Models

- Audio input uses `{"type": "input_audio", "input_audio": {"data": "<base64>", "format": "wav"}}`
- Use `modalities: ["text", "audio"]` for audio-capable models

### Model Context Windows

Different models have different context window sizes. When using large prompts + media:
- Monitor `max_tokens` + prompt_tokens to stay within limits
- Some models use `max_completion_tokens` instead of `max_tokens`

---

## Configuration File Parameters

These are the parameters available in mybot's `config.json`:

### agents.defaults

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `workspace` | string | "~/.mybot/workspace" | Path to workspace directory |
| `model` | string | "anthropic/claude-opus-4-5" | Default model to use |
| `max_tokens` | int | 8192 | Maximum tokens in response |
| `temperature` | float | 0.7 | Sampling temperature |
| `max_tool_iterations` | int | 20 | Maximum tool calling iterations |
| `memory_window` | int | 50 | Number of messages to keep in context |

### providers.*

Each provider supports these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | API key for the provider |
| `api_base` | string/null | Custom API base URL (overrides default) |
| `extra_headers` | dict/null | Additional headers to send with requests |

### Example Provider Configurations

```json
{
  "providers": {
    "openai": {
      "apiKey": "sk-...",
      "apiBase": null,
      "extraHeaders": null
    },
    "nvidia_nim": {
      "apiKey": "nvapi-...",
      "apiBase": "https://integrate.api.nvidia.com/v1",
      "extraHeaders": null
    },
    "anthropic": {
      "apiKey": "sk-ant-...",
      "apiBase": null,
      "extraHeaders": null
    },
    "deepseek": {
      "apiKey": "sk-...",
      "apiBase": null,
      "extraHeaders": null
    }
  }
}
```

---

## Using Parameters in Code

Parameters can be passed to LiteLLM completion calls:

```python
import litellm

# Basic usage
response = await litellm.acompletion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7,
    max_tokens=100
)

# With tools
response = await litellm.acompletion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {...}
        }
    }],
    tool_choice="auto"
)

# With vision
response = await litellm.acompletion(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
        ]
    }]
)

# With extended thinking (Anthropic)
response = await litellm.acompletion(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Solve this problem"}],
    thinking={"type": "enabled", "budget_tokens": 2048}
)
```

---

## Notes

1. **Parameter Compatibility**: Not all parameters work with all providers. Use `drop_params=True` to silently drop unsupported parameters.

2. **Provider Detection**: LiteLLM automatically detects the provider based on:
   - Model name keywords (e.g., "claude" → Anthropic, "gpt" → OpenAI)
   - API key prefix (e.g., "sk-or-" → OpenRouter)
   - API base URL keywords

3. **Environment Variables**: Some providers also read from environment variables:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `DEEPSEEK_API_KEY`
   - `MOONSHOT_API_KEY`
   - `NVIDIA_API_KEY`

4. **API Base**: Custom endpoints can be specified via the `api_base` parameter or provider config.

---

## References

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM Input Parameters](https://docs.litellm.ai/docs/completion/input)
- [Provider-Specific Parameters](https://docs.litellm.ai/docs/completion/provider_specific_params)
- [Thinking/Reasoning](https://docs.litellm.ai/docs/reasoning_content)
