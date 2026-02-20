# mybot Development Tasks

---

## Pending

### Testing / Bug Hunting

Active investigation for issues in the codebase.

---

## Documentation Plan

### Structure: `/docs/` Directory

```
docs/
├── index.md              # Main index / navigation
├── installation.md       # Installation: pip install -e .
├── quickstart.md        # Quick start guide (onboard, basic config)
├── cli.md               # CLI commands reference
├── configuration.md     # Full config.json reference
├── providers.md         # 18 LLM providers
├── channels.md          # Telegram & Email
├── agent.md             # Agent config (model, memory, tools)
├── workspace.md         # Bootstrap files (AGENTS.md, SOUL.md, USER.md, TOOLS.md)
├── skills.md            # Skills system
├── cron.md              # Cron service
├── heartbeat.md         # Heartbeat service
├── security.md          # Security (link to SECURITY.md)
└── parameters.md        # LLM params (link to parameters.md)
```

### Key Findings from Codebase

#### CLI Commands (11 commands)
| Command | Description |
|---------|-------------|
| `mybot onboard` | Initialize config and workspace |
| `mybot gateway` | Start service (cron, heartbeat, channels) |
| `mybot agent` | Interactive/direct agent mode |
| `mybot status` | Show current status |
| `mybot channels status` | Channel status |
| `mybot cron list` | List scheduled tasks |
| `mybot cron add` | Add task (--every, --cron, --at) |
| `mybot cron remove` | Remove task |
| `mybot cron enable` | Enable/disable task |
| `mybot cron run` | Run task manually |
| `mybot provider login` | OAuth login |

#### Bootstrap Files (workspace/)
Files loaded into agent context (in order):

| File | Purpose | Editable |
|------|---------|----------|
| `AGENTS.md` | Agent operational constraints/rules | ✅ User |
| `SOUL.md` | Bot personality | ✅ User |
| `USER.md` | User preferences | ✅ User |
| `TOOLS.md` | Tool documentation (for agent reference) | ✅ User |

#### Identity Section (hardcoded in context.py)
- Not in workspace - part of runtime identity
- Shows: current time, runtime info, workspace paths
- References: MEMORY.md, HISTORY.md, skills/

#### Memory/History (auto-managed)
| File | Purpose |
|------|---------|
| `memory/MEMORY.md` | Long-term memory (consolidated) |
| `memory/HISTORY.md` | Append-only conversation log |

#### Skills System
- Built-in: `mybot/skills/`
- Workspace: `workspace/skills/`
- Each skill: `skills/{name}/SKILL.md`
- `always=true` in frontmatter = always loaded

### Implementation Tasks

- [x] Create `docs/` directory
- [x] Create `docs/index.md` - navigation
- [x] Create `docs/installation.md` - pip install, virtualenv
- [x] Create `docs/quickstart.md` - onboard, basic config
- [x] Create `docs/cli.md` - all 11 CLI commands
- [x] Create `docs/configuration.md` - full config schema
- [x] Create `docs/providers.md` - 18 providers
- [x] Create `docs/channels.md` - Telegram + Email
- [x] Create `docs/agent.md` - model, temperature, memory_window, etc.
- [x] Create `docs/workspace.md` - bootstrap files (AGENTS.md, SOUL.md, USER.md, TOOLS.md), memory, history
- [x] Create `docs/skills.md` - skills system
- [x] Create `docs/cron.md` - cron service
- [x] Create `docs/heartbeat.md` - heartbeat service
- [x] Create `docs/security.md` - moved from root
- [x] Create `docs/parameters.md` - moved from root
- [x] Remove root SECURITY.md and parameters.md

---

## Completed Code Fixes

- ✅ `restrict_to_workspace` default → `True`
- ✅ Removed unused web tool config classes
- ✅ Wired up `web_search.max_results` from config
- ✅ Removed `IDENTITY.md` from BOOTSTRAP_FILES (doesn't exist)

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
