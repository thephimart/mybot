# Cron

Schedule tasks to run automatically.

## Overview

The cron service runs scheduled tasks through the agent. Only active when running `mybot gateway`.

## Schedule Types

### Every (Interval)

Run every N minutes/hours.

```bash
mybot cron add --every 30m "Check for new emails"
mybot cron add --every 2h "Generate daily summary"
```

### Cron Expression

Standard cron syntax.

```bash
# Daily at 9am
mybot cron add --cron "0 9 * * *" "Morning briefing"

# Every Monday at 9am
mybot cron add --cron "0 9 * * 1" "Weekly report"

# Every hour
mybot cron add --cron "0 * * * *" "Hourly check"
```

### At (One-time)

Run once at specific time.

```bash
mybot cron add --at "2026-01-01 12:00" "New year task"
```

## Commands

### List Tasks

```bash
mybot cron list
```

Shows: ID, schedule, enabled status, last run.

### Remove Task

```bash
mybot cron remove <task-id>
```

### Enable/Disable

```bash
mybot cron enable <task-id> true
mybot cron enable <task-id> false
```

### Run Now

```bash
mybot cron run <task-id>
```

## Task Output

Cron tasks can optionally deliver results:

```python
# Via the cron tool in agent:
cron --deliver --to telegram:123456 "Task complete!"
```

## Storage

Tasks are stored in `~/.mybot/data/cron/jobs.json`
