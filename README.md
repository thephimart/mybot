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
- A "supports everything" chatbot
- A place to pile on integrations

If you're looking for feature checklists, this project is not for you.

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
- Tool execution (file, shell, web search/fetch)
- Vision support (any vision-enabled model via Telegram, CLI -i)
- Speech-to-text (STT) via Telegram voice messages or CLI -a (local faster-whisper or Groq)
- Persistent memory
- Scheduling / cron
- Heartbeat (periodic agent wake-up)
- Minimal channels:
  - Telegram
  - Email
- CLI for local operation

Nothing else is considered "core".

---

## Gateway model (important)

mybot does **not** expose an HTTP API by default.

The "gateway" is a **channel-driven runtime**, not a REST server. It coordinates:
- the agent loop
- scheduling / cron
- heartbeat
- memory
- enabled I/O channels (CLI, Telegram, Email)

If no channel binds an external interface, no network port will be open.
This is intentional.

---

## Project structure

```
./
├── docs/                  # Documentation
├── mybot/                 # Core package
│   ├── agent/             # Core agent loop, context, memory
│   ├── bus/               # Internal event routing
│   ├── channels/          # I/O channels (Telegram, Email)
│   ├── cli/               # Command-line interface
│   ├── config/            # Configuration models
│   ├── cron/              # Scheduled tasks
│   ├── heartbeat/         # Periodic agent wake-up
│   ├── providers/         # LLM providers
│   ├── session/           # Conversation history
│   ├── skills/            # Built-in skills
│   └── utils/             # Helper utilities
├── tests/                 # Test suite
├── workspace/             # Template files (created on onboard)
├── LICENSE                # MIT License
├── pyproject.toml        # Project metadata and dependencies
└── README.md              # This file
```

If a directory doesn't justify its existence, it shouldn't be here.

---

## How to use mybot

The intended workflow is:

```
git clone mybot → rename → delete what you don't need → build yourbot
```

There is no official deployment story.
There is no canonical configuration.
There is no "recommended stack".

Those choices belong to you.

---

## Quick Start (example)

This is one way to get running — adapt as needed.

```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e .

# Initialize
mybot onboard

# Configure (edit ~/.mybot/config.json)
# Add your API key and model

# Run
mybot agent -m "Hello!"
```

**Security note:** Run mybot in its own virtual environment. At worst, it can only break its own environment.

---

## Documentation

- [Installation](docs/installation.md) - Setup and installation
- [Quick Start](docs/quickstart.md) - First-time setup guide
- [Configuration](docs/configuration.md) - Full config reference
- [Providers](docs/providers.md) - LLM provider setup (18 providers)
- [Channels](docs/channels.md) - Telegram and Email
- [CLI](docs/cli.md) - Command reference
- [Workspace](docs/workspace.md) - Bootstrap files (AGENTS.md, SOUL.md, etc.)
- [Skills](docs/skills.md) - Extending agent capabilities
- [Tools](docs/tools.md) - Tool configuration
- [Cron](docs/cron.md) - Scheduled tasks
- [Heartbeat](docs/heartbeat.md) - Periodic agent wake-up
- [Security](docs/security.md) - Security best practices
- [Parameters](docs/parameters.md) - LLM parameters

---

## Local LLMs

Local models (e.g. llama.cpp, Ollama, LM Studio) are supported.

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

## Future integrations (exploring)

- **Local TTS** - Text-to-speech using [kokoro](https://pypi.org/project/kokoro/) (runs locally)
- **Local image generation** - Image generation using [stable-diffusion-cpp-python](https://pypi.org/project/stable-diffusion-cpp-python/)

Under research/evaluation.

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

If you're wondering *"why doesn't mybot support X?"*
The answer is probably:

> Because **you** should add it — or decide you don't need it.

That's the point.
