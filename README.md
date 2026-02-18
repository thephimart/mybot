# mybot

**mybot** is a minimal, pure-Python bot core.

It provides only the fundamentals required to run an autonomous agent:
- an agent loop
- tools
- memory
- scheduling
- a small number of I/O channels

Everything else is intentionally left out.

If you need more, you add it.  
When you do, it becomes **yourbot**.

---

## What mybot is

- **A core**, not a framework
- **Pure Python** (no Node, no npm, no JS runtime)
- **Deliberately small** and readable
- **Designed to be forked**, not extended via plugins
- **Agent-first**, not chat-first

mybot is meant to live inside *your* repo, *your* environment, *your* constraints.

---

## What mybot is not

- A batteries-included assistant
- A platform or ecosystem
- A SaaS product
- A “supports everything” chatbot
- A place to pile on integrations

If you’re looking for feature checklists, this project is not for you.

---

## Design philosophy

1. **Minimal surface area**
   - Fewer abstractions
   - Fewer indirections
   - Fewer opinions

2. **Fork-first**
   - You are expected to copy this repo
   - Rename it
   - Change it freely

3. **Explicit over configurable**
   - Code changes beat config flags
   - Removing code is preferred to disabling it

4. **Security by reduction**
   - Less code → fewer bugs → smaller attack surface

---

## Included functionality

mybot intentionally includes only:

- Agent loop (LLM ↔ tools)
- Tool execution (including web, image, video, news, and book search)
- Vision, audio, and video support (for multimodal models like GPT-4o, Claude 4, Gemini)
- Persistent memory
- Scheduling / cron
- Minimal channels:
  - Telegram
  - Email
- Simple configuration
- CLI for local operation

Nothing else is considered “core”.

---

## Gateway model (important)

mybot does **not** expose an HTTP API by default.

The “gateway” is a **channel-driven runtime**, not a REST server. It coordinates:
- the agent loop
- scheduling / cron
- memory
- enabled I/O channels (CLI, Telegram, Email)

If no channel binds an external interface, no network port will be open.
This is intentional.

An HTTP ingress (e.g. `/message → agent loop`) may be added later as a new channel,
but it is **not part of the core**.

---

## Project structure

```
mybot/
├── agent/        # Core agent loop, context, memory, tools
├── tools/        # Built-in tools
├── channels/     # Minimal I/O (Telegram, Email)
├── cron/         # Scheduled tasks
├── bus/          # Internal event routing
├── providers/    # LLM providers
├── config/       # Configuration models
└── cli/          # Command-line interface
```

If a directory doesn’t justify its existence, it shouldn’t be here.

---

## How to use mybot

The intended workflow is:

```text
git clone mybot → rename → delete what you don’t need → build yourbot
```

There is no official deployment story.
There is no canonical configuration.
There is no “recommended stack”.

Those choices belong to you.

---

## Local LLMs

Local models (e.g. llama.cpp, Ollama, LM Studio) are supported via the `custom` provider.

Routing is determined by the configured `apiBase`.
If the endpoint does not require an API key, any non-empty value may be used.

Model name handling depends on the backend:
- some local runtimes ignore it
- others (e.g. Ollama) use it for routing

This allows mybot to work with any OpenAI-compatible local or remote endpoint
without special casing.

---

## Line count

mybot is intentionally small.

If the codebase starts growing without a very good reason, something has gone wrong.

---

## Origin & attribution

mybot began as a **heavily reduced refactor** of the open-source project **nanobot**.

* Original project: [https://github.com/HKUDS/nanobot](https://github.com/HKUDS/nanobot)
* License: MIT (retained)

The codebase has been reshaped, reduced, or rewritten to serve a different goal:
a stripped-down, fork-first Python bot core.

---

## License

MIT License.
Do whatever you want — just keep the notice.

---

## Final note

If you’re wondering *“why doesn’t mybot support X?”*
The answer is probably:

> Because **you** should add it — or decide you don’t need it.

That’s the point.
