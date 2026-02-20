# Skills

Skills extend the agent's capabilities.

## Overview

Skills are markdown files that define capabilities the agent can use.

## Skill Locations

### Built-in Skills

Located in `mybot/skills/` (package directory)

### Workspace Skills

Located in `workspace/skills/` (user directory)

## Creating a Skill

Create a directory with `SKILL.md`:

```
workspace/skills/my-skill/
└── SKILL.md
```

## SKILL.md Format

```markdown
---
name: My Skill
description: What this skill does
always: false
requires:
  bins: ["curl"]
  env: ["API_KEY"]
---

# My Skill

Instructions for using this skill...

## Usage

Do something specific...
```

### Frontmatter

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill name |
| `description` | string | Brief description |
| `always` | bool | Always load in context (default: false) |
| `requires.bins` | array | Required binaries |
| `requires.env` | array | Required environment variables |

## Always-Loaded Skills

Set `always: true` in frontmatter to always include the skill in context.

```yaml
---
name: Memory
description: Long-term memory management
always: true
---
```

## Using Skills

1. Skills are listed in the system prompt
2. Agent reads `SKILL.md` when needed
3. Agent can then use the skill's capabilities

## Example Skills

See built-in skills in `mybot/skills/` for examples.
