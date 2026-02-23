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
- Image support (any vision-enabled model via Telegram  or 'CLI -i "image-file"')
- Speech-to-text (STT) via Telegram voice messages or 'CLI -a "audio-file"'
  - (local faster-whisper or Groq)
- Text-to-speech (TTS) via 'speak' tool (local kokoro)
  - Agent generates audio, sends via message tool with media param
- Subagent with independent configuration
  - Used to offload long-running or token-heavy work from the main agent loop
- Persistent memory
- Scheduling / cron
- Heartbeat (periodic agent wake-up)
- Minimal channels:
  - Telegram
  - Email
- CLI for local operation
- Subagent with independent configuration
  - Used to offload long-running or token-heavy work from the main agent loop
- Optional systemd user service mode enabling remotely self-improving, skill-building agents.
  - [Systemd User Service](docs/restart.md)

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
- Optional systemd user service mode remote restart

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

- [Documentation Index](docs/index.md) - Overview and navigation

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

**mybot is intentionally small.**

A compact codebase is a design goal: if the line count grows without a very good reason, something has gone wrong.  
Most complexity is pushed into **skills**, **configuration**, and **external providers**, not the core agent loop.

**Current core line count (v0.4.1):**
```
agent/      1451
tools/      1274
bus/        122
config/     374
cron/       429
heartbeat/  135
session/    207
utils/      85
(root)      14

Core total: 4091
```
> Excludes optional integrations: `channels/`, `cli/`, `providers/`

**Why this matters**

- Smaller surface area → easier reasoning and auditing  
- Fewer hidden side effects in the core loop  
- Faster onboarding for contributors  
- Safer self-modifying and skill-building behavior  

If this number starts climbing without a clear architectural justification, it’s a signal to stop and refactor.

---

## Future integrations (exploring)

- **Local LLM multi-instance support** – Allow `.agent` and `.subagent` suffixed local providers (e.g. `llamacpp`, `lmstudio`, other fixed-model OpenAI-compatible servers) to run the main agent and subagent on separate local API endpoints. This enables isolation between agent and subagent workloads when local inference servers are bound to a single loaded model per endpoint (for example `llamacpp.agent` → `http://192.168.1.2:8001/v1`, `llamacpp.subagent` → `http://192.168.1.2:8002/v1`).

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
