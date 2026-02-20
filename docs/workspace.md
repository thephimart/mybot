# Workspace

The workspace is where mybot reads and writes files. Default: `~/.mybot/workspace`

## Directory Structure

```
~/.mybot/workspace/
├── AGENTS.md        # Agent operational rules
├── SOUL.md          # Bot personality
├── USER.md          # User preferences
├── TOOLS.md         # Tool documentation (for agent)
├── HEARTBEAT.md     # Periodic tasks (optional)
├── memory/
│   ├── MEMORY.md    # Long-term memory
│   └── HISTORY.md   # Conversation history
└── skills/          # Custom skills (optional)
    └── {skill-name}/
        └── SKILL.md
```

## Bootstrap Files

These files are loaded into the agent's system prompt (in order):

### AGENTS.md

Operational constraints and rules for the agent.

```markdown
# Agent Rules

This file defines **operational constraints** for agents running inside mybot.

## Scope
- Operate only within documented capabilities
- Do not assume tools, skills, files, or features exist

## Tools & Skills
- Available tools are defined exclusively in `TOOLS.md`
- Available skills are those present in `skills/` directories
```

### SOUL.md

Bot personality and character.

```markdown
# Bot Personality

You are a helpful, concise assistant.
```

### USER.md

User preferences and context.

```markdown
# User Preferences

- Preferred language: English
- Time zone: UTC
```

### TOOLS.md

Tool documentation for agent reference. The agent reads this to understand available tools.

See [workspace/TOOLS.md](../../workspace/TOOLS.md) for the default version.

---

## Memory

### memory/MEMORY.md

Long-term memory. The agent writes important information here using the memory skill.

### memory/HISTORY.md

Append-only conversation log. Grep-searchable.

---

## Identity (Runtime)

The agent also receives a runtime identity section with:
- Current time
- Runtime info (OS, machine, Python version)
- Workspace paths (memory, history, skills)

This is hardcoded in the agent and not editable.
