"""Audio transcription using faster-whisper."""

import asyncio
import tempfile
from pathlib import Path
from typing import Any

from loguru import logger


class Transcriber:
    """Async wrapper for faster-whisper transcription."""

    def __init__(
        self,
        model: str = "base",
        device: str = "auto",
        compute_type: str = "int8",
    ):
        self.model_name = model
        self.device = device
        self.compute_type = compute_type
        self._model: Any = None

    def _get_model(self) -> Any:
        """Lazy-load the Whisper model."""
        if self._model is None:
            from faster_whisper import WhisperModel

            logger.info(f"Loading faster-whisper model: {self.model_name}")
            self._model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type,
            )
            logger.info("faster-whisper model loaded")
        return self._model

    async def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file to text with optimized settings."""
        import os

        file_size = os.path.getsize(audio_path)
        logger.info(f"Transcribing audio file, size: {file_size} bytes")

        model = self._get_model()

        # Run transcription in executor to avoid blocking
        loop = asyncio.get_event_loop()
        segments, info = await loop.run_in_executor(
            None,
            lambda: model.transcribe(
                audio_path,
                beam_size=1,
                best_of=1,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
            ),
        )

        # Wait for segments generator
        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())

        result = " ".join(text_parts)
        logger.info(f"Transcription result: '{result}'")
        return result

    async def transcribe_base64(self, audio_b64: str, format: str = "wav") -> str:
        """Transcribe base64-encoded audio data."""
        audio_bytes = __import__("base64").b64decode(audio_b64)

        with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            return await self.transcribe(tmp_path)
        finally:
            try:
                Path(tmp_path).unlink()
            except Exception:
                pass


_global_transcriber: Transcriber | None = None


def get_transcriber(
    model: str = "base",
    device: str = "auto",
    compute_type: str = "int8",
) -> Transcriber:
    """Get or create global transcriber instance."""
    global _global_transcriber

    if _global_transcriber is None:
        _global_transcriber = Transcriber(
            model=model,
            device=device,
            compute_type=compute_type,
        )

    return _global_transcriber
