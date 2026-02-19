# mybot Development Tasks

This file tracks issues and desired changes identified during code reviews.

---

## Security & Access Control

### restrict_to_workspace Behavior

**Issue:** Current implementation restricts to `~/.mybot/workspace` ONLY when `restrict_to_workspace=true`.

**Expected Behavior:**
- `restrict_to_workspace=true` → agent has full access to ALL subdirectories of `~/.mybot/*`
- `restrict_to_workspace=true` → agent has READ-ONLY access to install directory (`./mybot`)
- Agent should **NEVER** have access to:
  - `~/.mybot/config.json`
  - ANY `.env` files across the entire filesystem

**Files to modify:**
- `mybot/agent/tools/filesystem.py` - update `_resolve_path()` to handle multiple allowed directories
- `mybot/agent/tools/shell.py` - update `ExecTool._guard_command()` path checking
- `mybot/agent/loop.py` - pass multiple allowed directories to tools

---

### Lock Down Sensitive Files

**Issue:** Agent can potentially read `config.json` and `.env` files via file tools.

**Requirements:**
1. Agent tools must explicitly block access to:
   - `~/.mybot/config.json`
   - Any `.env` files anywhere on the filesystem
2. Only these commands can access config.json:
   - `mybot onboard` - write access
   - `mybot status` - read access (without apiKey values)

**Implementation:**
- Create `load_config_safe()` in `mybot/config/loader.py` that strips `apiKey` fields before returning
- Update `_resolve_path()` to check against blocked files/directories
- Add `.env` pattern matching to blocklist

---

### Status Command API Key Handling

**Issue:** `mybot status` loads full config including apiKey values into memory.

**Desired:** Create `load_config_safe()` that:
- Reads config.json
- Strips all `apiKey` fields
- Keeps `api_base` (non-sensitive)
- Returns safe config for display

**Files to modify:**
- `mybot/config/loader.py` - add `load_config_safe()` function
- `mybot/cli/commands.py` - use `load_config_safe()` in status command

---

## Documentation

### AGENTS.md Updates Needed

- [x] Added instruction to check TOOLS.md and skills/ first
- [x] Clarified skills directory paths
- [x] Updated heartbeat section to note gateway-only
- [x] Added cron CLI usage examples

### TOOLS.md Updates Needed

- [x] Added "Tool Availability by Mode" table
- [x] Fixed cron documentation (CLI vs native tool)
- [x] Added note about heartbeat being gateway-only
- [x] Updated message tool context requirements

---

## Minor Issues

### CLI Help Text

- [x] `mybot agent --help` now mentions "interactive mode"

---

## Configuration

### Exec Timeout Default

**Issue:** Current default timeout for `exec` tool is 60 seconds, which is too short for long-running commands (e.g., `pip install torch`, docker builds, compiling code).

**Recommended:** Increase default timeout from 60s to 300s (5 minutes).

**Rationale:**
- 60s: Too short for any meaningful package installation or build
- 300s (5 min): Enough for most `pip install`, moderate builds, git clones
- 1200s (20 min): Possibly too long - could hide hung processes

**Files to modify:**
- `mybot/config/schema.py` - change `ExecToolConfig.timeout` default from 60 to 300

---

## Notes

### Dependencies

All required packages are in main dependencies list in pyproject.toml:
- `ddgs` - web search
- `readability-lxml` - HTML parsing
- `faster-whisper` - local transcription
- `croniter` - cron expressions
- `mcp` - MCP client

No changes needed - these are required deps.

### Email consent_granted

By design - email channel requires explicit `consent_granted=true`. Documentation should mention this.

### faster-whisper Model Storage

Uses HuggingFace cache (~/.cache/huggingface/). No changes needed - allows sharing models across system.

### .env Files

Code does NOT load .env files. Uses environment variables via `os.environ.get()`. This is secure by default.
