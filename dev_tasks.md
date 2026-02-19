# mybot Development Tasks

---

## Pending

### restrict_to_workspace Behavior (HIGH)

Implement proper workspace restriction when `restrict_to_workspace=true`:
- `~/.mybot/*` → full read/write (except config.json)
- `*/mybot/*` → read-only
- Block `~/.mybot/config.json` always

**Files:** `mybot/agent/tools/filesystem.py`, `shell.py`, `loop.py`

---

### Status Command API Key Handling (HIGH)

`mybot status` should not display apiKey values.

**Files:** `mybot/config/loader.py`, `mybot/cli/commands.py`

---

## Future

### Kokoro TTS Integration

Research local TTS with kokoro package. See https://pypi.org/project/kokoro/

---

### Stable Diffusion CPP Integration

Research local image generation. See https://pypi.org/project/stable-diffusion-cpp-python/

---

## Completed

- ✅ Exec timeout default: 60s → 300s
- ✅ Trim ddgs: removed image/video/news/books search
- ✅ TOOLS.md: tool availability table, web tools docs
- ✅ AGENTS.md: check TOOLS.md first
