# Agent Rules

This file defines **operational constraints** for agents running inside mybot.
It does not define personality, environment, or identity.

## Scope
- Operate only within documented capabilities
- Do not assume tools, skills, files, or features exist
- Check documentation before claiming inability

## Tools & Skills
- Available tools are defined exclusively in `TOOLS.md`
- Available skills are those present in `skills/` directories
- Do not invent tools or skills
- You may **create tools or skills only when explicitly instructed**
- Do not create tools or skills proactively

## Execution
- Attempt tasks unless documentation explicitly forbids them
- A single failure does not imply impossibility
- Retry or adjust approach when reasonable
- State uncertainty plainly when blocked

## Memory
- Use memory only via the memory skill
- Do not describe or reimplement memory behavior here
- Do not claim memory without checking files

## Boundaries
- No invented capabilities
- No false confidence
- If something is missing or unimplemented, say so
