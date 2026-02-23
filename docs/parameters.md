## LiteLLM Parameters (mybot)

mybot uses **LiteLLM as a provider abstraction layer**, but intentionally exposes **only a minimal, stable subset** of parameters.

> **Current behavior (important)**  
> At present, **only `max_tokens` and `temperature` are forwarded** from mybot to the underlying provider API.  
> All other LiteLLM parameters are **ignored**, even if specified.

Support for additional parameters may be added in future versions as they become justified by real use cases.

---

## Supported Parameters (Current)

These parameters are configurable via `config.json` and are passed through to LiteLLM and the provider.

| Parameter | Type | Default | Description |
|---------|------|---------|-------------|
| `max_tokens` | int | 8192 | Maximum tokens in the model response |
| `temperature` | float | 0.7 | Sampling randomness (0 = deterministic) |

These apply equally to:
- main agent
- subagents (via inheritance / spawn resolution)

---

## Not Yet Supported (Ignored)

LiteLLM supports many additional parameters, but **mybot does not currently forward or manage them**, including but not limited to:

- Sampling controls (`top_p`, `top_k`, `frequency_penalty`, `presence_penalty`)
- Tool / function call controls (`tools`, `tool_choice`, `parallel_tool_calls`)
- Reasoning / thinking flags
- Streaming options
- Provider-specific options
- Extra HTTP headers
- Retry or caching controls

Specifying these will **not error**, but they will **have no effect**.

This is intentional: mybot favors **explicit behavior and small surface area** over exposing every provider knob.

---

## Why This Is Restricted

mybot’s design goals:

- Keep the **agent loop predictable**
- Avoid provider-specific branching logic
- Prevent config drift between providers
- Make self-modifying and skill-building agents safer

Advanced behaviors (reasoning modes, tools, streaming, etc.) are expected to be implemented **as agent logic or skills**, not configuration flags.

---

## Future Expansion

Additional parameters may be selectively enabled when:

- They are **provider-agnostic**
- They serve a **clear agent-level purpose**
- They do not meaningfully increase complexity or ambiguity

When enabled, they will be documented explicitly here.

---

## Reference (Upstream)

For completeness, LiteLLM supports a wide range of parameters across providers.

If you are modifying mybot itself or building a fork that exposes more of LiteLLM, consult:

- https://docs.litellm.ai/docs/completion/input
- https://docs.litellm.ai/docs/completion/provider_specific_params

These references describe **LiteLLM capabilities**, not mybot behavior.

---

> **TL;DR**  
> **LiteLLM is powerful. mybot is intentionally not.**  
> If you need more parameters, you are expected to add them deliberately — or fork.