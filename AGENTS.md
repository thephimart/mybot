# Agent Instructions for mybot

This file provides guidelines for agentic coding agents working on the mybot codebase.

## Project Overview

mybot is an ultra-lightweight personal AI assistant (~4,000 lines) built with Python 3.11+. It uses a message bus architecture with pluggable channels (Telegram, Email) and supports LLM providers via litellm.

## Environment Setup

### Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Installation (Development)
```bash
pip install -e ".[dev]"
```

## Build, Lint, and Test Commands

### Running Tests
```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_commands.py

# Run a single test function
pytest tests/test_commands.py::test_onboard_fresh_install

# Run tests matching a pattern
pytest -k "test_onboard"

# Run with verbose output
pytest -v
```

### Linting and Formatting
```bash
# Run ruff linter (configured in pyproject.toml)
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Check line length (100 chars) and formatting
ruff format --check .
```

### Building
```bash
# Build wheel with hatch
hatch build

# Install locally after build
pip install dist/mybot_ai-*.whl
```

## Code Style Guidelines

### General Principles
- Be concise and direct — avoid unnecessary abstractions
- Prioritize readability over cleverness
- Keep functions focused and small (< 100 lines preferred)
- Document complex logic with docstrings, not comments

### Imports
Organize imports in this order (use isort conventions via ruff):
1. Standard library (`asyncio`, `json`, `pathlib`)
2. Third-party packages (`loguru`, `typer`, `pydantic`)
3. Local mybot modules (`mybot.agent`, `mybot.bus`)

```python
import asyncio
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic import BaseModel

from mybot.bus.events import InboundMessage, OutboundMessage
from mybot.bus.queue import MessageBus
```

### Type Hints
Use Python 3.11+ union syntax:
```python
# Good
def foo(x: str | None) -> int | None: ...

# Avoid
from typing import Optional
def foo(x: Optional[str]) -> Optional[int]: ...
```

Use `Any` sparingly — prefer concrete types. Use `dict[str, Any]` for loosely-typed dictionaries.

### Naming Conventions
- **Classes**: `CamelCase` (e.g., `AgentLoop`, `ToolRegistry`)
- **Functions/variables**: `snake_case` (e.g., `get_or_create`, `max_iterations`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `EXIT_COMMANDS`)
- **Private methods**: Prefix with underscore (e.g., `_register_default_tools`)
- **Abstract properties**: Use `@property` with `@abstractmethod` for interface definition

### Error Handling
- Use `loguru.logger` for logging — it's already configured
- Catch specific exceptions, not bare `Exception`
- Provide meaningful error messages
- Return graceful failures rather than crashing

```python
try:
    result = await self.provider.chat(...)
except httpx.TimeoutException:
    logger.warning("Provider timeout, retrying...")
    # handle retry
except Exception as e:
    logger.error(f"Unexpected error in chat: {e}")
    return "An error occurred processing your request."
```

### Docstrings
Follow Google-style docstrings for complex functions:

```python
async def process_message(self, msg: InboundMessage) -> OutboundMessage | None:
    """
    Process a single inbound message.

    Args:
        msg: The inbound message to process.

    Returns:
        The response message, or None if no response needed.
    """
```

Keep simple methods uncommented if the code is self-explanatory.

### Pydantic Models
- Use `BaseModel` for configuration and data transfer objects
- Use `pydantic-settings` for app settings
- Define validation in field definitions, not in `__init__`

```python
class Config(BaseModel):
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
```

### Async/Await
- Use `asyncio` for concurrency — mybot is async-first
- Always `await` async functions; never use `.result()` or `.wait()`
- Use `asyncio.create_task()` for fire-and-forget background tasks

### Testing
- Place tests in `tests/` directory
- Use `pytest` with `pytest-asyncio` for async tests
- Use `pytest.mark.parametrize` for testing multiple inputs
- Mock external dependencies (LLM providers, file I/O)
- Use `typer.testing.CliRunner` for CLI tests

```python
from typer.testing import CliRunner
from mybot.cli.commands import app

runner = CliRunner()

def test_something():
    result = runner.invoke(app, ["some-command"])
    assert result.exit_code == 0
```

### Channel Implementations
When adding new channels:
1. Subclass `BaseChannel` from `mybot.channels.base`
2. Implement `start()`, `stop()`, `send()` — all async
3. Use `_handle_message()` to validate and forward inbound messages
4. Set `name` class attribute to the channel identifier

### Tool Implementations
When adding new tools:
1. Subclass `Tool` from `mybot.agent.tools.base`
2. Implement `name`, `description`, `parameters` (JSON Schema), and `execute()`
3. Register in `ToolRegistry` in the agent loop
4. Use type-safe parameter validation via `validate_params()`

### File Structure
```
mybot/
├── agent/          # Core agent logic (loop, context, memory, subagents)
├── agent/tools/   # Tool implementations (file, shell, web, etc.)
├── bus/            # Message bus (events, queue)
├── channels/       # Channel integrations (telegram, email)
├── providers/      # LLM providers (openai, litellm, local...)
├── skills/         # Skill definitions (markdown + scripts)
├── cli/            # CLI commands (typer)
├── config/         # Configuration loading and schema
├── cron/           # Scheduled task service
├── heartbeat/      # Background periodic tasks
├── session/        # Session management
└── utils/          # Helper utilities
```

### Configuration
- Store runtime config in JSON via `mybot.config.loader`
- Use `Config` pydantic model in `mybot.config.schema`
- Workspace files go in user-configured workspace directory
