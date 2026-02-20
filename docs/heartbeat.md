# Heartbeat

Periodic agent wake-up to check for tasks.

## Overview

The heartbeat service wakes the agent every 30 minutes to check for work. Only active when running `mybot gateway`.

## How It Works

1. Every 30 minutes, the agent reads `HEARTBEAT.md` from the workspace
2. If tasks are listed, the agent executes them
3. If nothing needs attention, agent responds with `HEARTBEAT_OK`

## HEARTBEAT.md

Create `workspace/HEARTBEAT.md`:

```markdown
# Tasks

- [ ] Check new emails
- [ ] Review calendar

<!-- Leave empty or only headers for no tasks -->
```

### Format

- Tasks as checkboxes: `- [ ]` or `- [x]`
- Plain text instructions
- Empty file = nothing to do
- Only headers = nothing to do

## Configuration

Currently fixed at 30-minute intervals. Future versions may support customization.

## Use Cases

- Periodic email checks
- News aggregation
- System monitoring
- Scheduled reports
