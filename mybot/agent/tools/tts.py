"""Text-to-speech tool for generating audio from text."""

from pathlib import Path
from typing import Any

from mybot.agent.tools.base import Tool
from mybot.providers.tts import get_tts_provider


class TTSTool(Tool):
    """Generate speech from text using local Kokoro TTS."""

    def __init__(
        self,
        workspace: Path | None = None,
        voice: str = "af_heart",
        lang_code: str = "b",
    ):
        self.workspace = workspace or Path.home() / ".mybot" / "workspace"
        self.voice = voice
        self.lang_code = lang_code
        self._provider = None

    @property
    def name(self) -> str:
        return "speak"

    @property
    def description(self) -> str:
        return "Generate speech from text. Returns a file path to the audio. Use with message tool to send."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to synthesize into speech",
                },
                "voice": {
                    "type": "string",
                    "description": "Voice preset (default: af_heart)",
                },
                "lang_code": {
                    "type": "string",
                    "description": "Language code (default: b)",
                },
            },
            "required": ["text"],
        }

    async def execute(self, text: str, voice: str | None = None, lang_code: str | None = None, **kwargs: Any) -> str:
        if not text or not text.strip():
            return "Error: text cannot be empty"

        voice = voice or self.voice
        lang_code = lang_code or self.lang_code

        output_dir = self.workspace / "media" / "tts"

        try:
            provider = get_tts_provider(voice=voice, lang_code=lang_code)
            output_path = provider.speak(text, output_dir=output_dir)

            return str(output_path)

        except RuntimeError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: TTS failed: {e}"
