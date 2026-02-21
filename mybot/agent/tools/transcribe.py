"""Transcribe tool for audio files."""

from pathlib import Path
from typing import Any

from mybot.agent.tools.base import Tool
from mybot.providers.transcription import get_transcriber


class TranscribeTool(Tool):
    """Transcribe audio files to text using faster-whisper or Groq."""

    def __init__(self, use_local: bool = True, whisper_model: str = "base", device: str = "cpu"):
        self.use_local = use_local
        self.whisper_model = whisper_model
        self.device = device

    @property
    def name(self) -> str:
        return "transcribe_audio"

    @property
    def description(self) -> str:
        return "Transcribe an audio file to text. Supports .ogg, .wav, .mp3 files."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the audio file to transcribe",
                },
                "language": {
                    "type": "string",
                    "description": "Optional language code (e.g., 'en', 'th', 'auto')",
                },
            },
            "required": ["path"],
        }

    async def execute(self, path: str, language: str | None = None, **kwargs: Any) -> str:
        file_path = Path(path)

        if not file_path.exists():
            return f"Error: File not found: {path}"

        if not file_path.is_file():
            return f"Error: Not a file: {path}"

        try:
            transcriber = get_transcriber(
                use_local=self.use_local,
                whisper_model=self.whisper_model,
                device=self.device,
            )

            result = await transcriber.transcribe(file_path)

            if not result:
                return "Error: No transcription generated"

            return result

        except Exception as e:
            return f"Error: Transcription failed: {e}"
