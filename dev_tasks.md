# mybot Development Tasks

---

## Pending

### Testing / Bug Hunting

Active investigation for issues in the codebase.

---

## Documentation Coverage Report

### Executive Summary

This report compares the existing user-facing documentation (README.md, SECURITY.md, parameters.md) against the actual codebase to identify gaps.

---

## Part 1: Research Findings

### Installation

```bash
git clone <mybot-repo>
cd mybot
pip install -e .
```

### Onboard Process

**Command:** `mybot onboard`

**Creates:**
- `~/.mybot/config.json` - Main configuration file
- `~/.mybot/workspace/` - Working directory with templates:
  - `AGENTS.md` - Agent rules/instructions
  - `SOUL.md` - Bot personality
  - `USER.md` - User preferences
  - `TOOLS.md` - Tool documentation (for agent reference)
  - `HEARTBEAT.md` - Periodic tasks (for heartbeat service)
  - `memory/` - Directory for memory files

### Gateway Command

**What it does:**
Starts the full mybot service as a long-running process with:
- **Agent loop** - Processes messages through LLM
- **Cron service** - Scheduled/periodic tasks
- **Heartbeat service** - Wakes every 30 minutes to check HEARTBEAT.md
- **Channel manager** - Telegram and/or Email integrations
- **Session manager** - Conversation history

**Port:** Default 18790 (configurable via `--port`)

**Use case:** Run as a persistent service (daemon) to receive messages from Telegram/Email.

### restrict_to_workspace Default

**Current:** `False` (in `mybot/config/schema.py:177`)

**Issue:** User wants this to be `True` by default for security.

---

### Tools Config Issue

**Problem:** Schema still contains removed tool configs:
- `ImageSearchConfig` (line 123)
- `VideoSearchConfig` (line 129)
- `NewsSearchConfig` (line 135)
- `BooksSearchConfig` (line 141)
- `WebToolsConfig.images/videos/news/books` (lines 151-154)

**Actual tools registered:**
- `web_search` - Uses `max_results=5` default (not from config)
- `web_fetch` - No config options

---

## Part 2: Required Configuration

### Minimum Required to Run

**Option 1: CLI mode (`mybot agent`)**
```json
{
  "agents": {
    "defaults": {
      "model": "provider/model-name"
    }
  },
  "providers": {
    "<provider>": {
      "apiKey": "your-api-key"
    }
  }
}
```

**Option 2: Gateway mode (`mybot gateway`)**
- Same as above + at least one channel enabled

### agents.defaults

| Setting | Required | Default | Description |
|---------|----------|---------|-------------|
| `workspace` | No | ~/.mybot/workspace | Working directory |
| `model` | **Yes** | anthropic/claude-opus-4-5 | LLM model name |
| `provider` | No | auto-detect | Explicit provider (e.g., "ollama", "openai") |
| `max_tokens` | No | 8192 | Max response tokens |
| `temperature` | No | 0.7 | Sampling temperature |
| `max_tool_iterations` | No | 20 | Max tool calls per message |
| `memory_window` | No | 50 | Messages in context |

### channels.telegram

| Setting | Required | Default | Description |
|---------|----------|---------|-------------|
| `enabled` | No | false | Enable Telegram channel |
| `token` | **If enabled** | - | Bot token from @BotFather |
| `allow_from` | **If enabled** | [] | Allowed usernames/IDs |
| `proxy` | No | null | HTTP/SOCKS5 proxy URL |

### transcriber

| Setting | Required | Default | Description |
|---------|----------|---------|-------------|
| `use_local` | No | true | true=faster-whisper, false=Groq API |
| `whisper_model` | If use_local=true | base | tiny/base/small/medium/large-v3 |
| `device` | If use_local=true | cpu | cpu/cuda/auto |

### tools.restrict_to_workspace

| Setting | Required | Default | Description |
|---------|----------|---------|-------------|
| `restrict_to_workspace` | No | **false** (needs fix) | Restrict file/exec to workspace |

---

## Part 3: Implementation Plans

### Plan 1: Change restrict_to_workspace Default to True

**File:** `mybot/config/schema.py`

**Change:** Line 177
```python
# Before:
restrict_to_workspace: bool = False

# After:
restrict_to_workspace: bool = True
```

**Risk:** LOW - Simple config change, affects new installs only.

---

### Plan 2: Remove Unused Tool Config Classes

**File:** `mybot/config/schema.py`

**Remove:**
- Lines 123-154: `ImageSearchConfig`, `VideoSearchConfig`, `NewsSearchConfig`, `BooksSearchConfig`, `WebToolsConfig`
- Remove `images`, `videos`, `news`, `books` from `WebToolsConfig`
- Keep only `search: WebSearchConfig`

**Code to remove:**
```python
class ImageSearchConfig(BaseModel):
    """Web image search configuration."""
    max_results: int = 5

class VideoSearchConfig(BaseModel):
    """Web video search configuration."""
    max_results: int = 5

class NewsSearchConfig(BaseModel):
    """Web news search configuration."""
    max_results: int = 5

class BooksSearchConfig(BaseModel):
    """Web books search configuration."""
    max_results: int = 5

class WebToolsConfig(BaseModel):
    """Web tools configuration."""
    search: WebSearchConfig = Field(default_factory=WebSearchConfig)
    images: ImageSearchConfig = Field(default_factory=ImageSearchConfig)  # REMOVE
    videos: VideoSearchConfig = Field(default_factory=VideoSearchConfig)  # REMOVE
    news: NewsSearchConfig = Field(default_factory=NewsSearchConfig)  # REMOVE
    books: BooksSearchConfig = Field(default_factory=BooksSearchConfig)  # REMOVE
```

**Risk:** LOW - Removing unused config classes.

---

### Plan 3: Wire Up Web Search Config

**File:** `mybot/agent/loop.py`

**Change:** Pass config to WebSearchTool

**Current (line 111):**
```python
self.tools.register(WebSearchTool())
```

**After:**
```python
self.tools.register(WebSearchTool(max_results=config.tools.web.search.max_results))
```

**Risk:** MEDIUM - Adds dependency on config in loop.py

---

## Part 4: Action Items

### Documentation Updates

- [ ] Add CLI commands section to README.md
- [ ] Document full config.json schema
- [ ] List all 18 providers with detection details
- [ ] Reference workspace bootstrap files in README.md
- [ ] Document channel configuration options
- [ ] Add cron/heartbeat/service documentation

### Code Fixes

- [ ] **Plan 1:** Change restrict_to_workspace default to True
- [ ] **Plan 2:** Remove unused tool config classes
- [ ] **Plan 3:** Wire up web search config (optional)

---

## Future

### Kokoro TTS Integration

Research local TTS with kokoro package. See https://pypi.org/project/kokoro/

---

### Stable Diffusion CPP Integration

Research local image generation. See https://pypi.org/project/stable-diffusion-cpp-python/

---

## Completed

(All completed tasks moved to git history)
