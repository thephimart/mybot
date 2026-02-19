"""Voice transcription providers: local (faster-whisper) and cloud (Groq API)."""

import os
from pathlib import Path

import httpx
from loguru import logger


class GroqTranscriptionProvider:
    """
    Voice transcription provider using Groq's Whisper API.

    Groq offers extremely fast transcription with a generous free tier.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"

    async def transcribe(self, file_path: str | Path) -> str:
        """
        Transcribe an audio file using Groq.

        Args:
            file_path: Path to the audio file.

        Returns:
            Transcribed text.
        """
        if not self.api_key:
            logger.warning("Groq API key not configured for transcription")
            return ""

        path = Path(file_path)
        if not path.exists():
            logger.error(f"Audio file not found: {file_path}")
            return ""

        try:
            async with httpx.AsyncClient() as client:
                with open(path, "rb") as f:
                    files = {
                        "file": (path.name, f),
                        "model": (None, "whisper-large-v3"),
                    }
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                    }

                    response = await client.post(
                        self.api_url, headers=headers, files=files, timeout=60.0
                    )

                    response.raise_for_status()
                    data = response.json()
                    return data.get("text", "")

        except Exception as e:
            logger.error(f"Groq transcription error: {e}")
            return ""


class LocalTranscriptionProvider:
    """
    Local voice transcription using faster-whisper.

    Automatically selects compute type based on device:
    - cpu: int8 (fastest on CPU)
    - cuda/auto: float16 (requires GPU)
    """

    def __init__(self, whisper_model: str = "base", device: str = "cpu"):
        self.whisper_model = whisper_model
        self.device = device
        self._model = None

    def _get_compute_type(self) -> str:
        """Select compute type based on device."""
        if self.device in ("cuda", "auto"):
            return "float16"
        return "int8"

    def _load_model(self):
        """Load or reuse cached model."""
        if self._model is None:
            try:
                from faster_whisper import WhisperModel

                compute_type = self._get_compute_type()
                logger.info(
                    f"Loading faster-whisper model: {self.whisper_model}, "
                    f"device: {self.device}, compute: {compute_type}"
                )
                self._model = WhisperModel(
                    self.whisper_model,
                    device=self.device,
                    compute_type=compute_type,
                )
            except Exception as e:
                logger.error(f"Failed to load faster-whisper model: {e}")
                raise
        return self._model

    async def transcribe(self, file_path: str | Path) -> str:
        """
        Transcribe an audio file using faster-whisper.

        Args:
            file_path: Path to the audio file.

        Returns:
            Transcribed text.
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Audio file not found: {file_path}")
            return ""

        try:
            model = self._load_model()
            logger.info(f"Transcribing: {path.name}")

            segments, _ = model.transcribe(
                str(path),
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
            )

            # Collect all segments
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text.strip())

            result = " ".join(text_parts)
            logger.info(f"Transcription complete: {result[:50]}..." if result else "Empty transcription")
            return result

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""


# Singleton instances for reuse
_local_transcriber: LocalTranscriptionProvider | None = None
_groq_transcriber: GroqTranscriptionProvider | None = None


def get_transcriber(
    use_local: bool = True,
    whisper_model: str = "base",
    device: str = "cpu",
    groq_api_key: str | None = None,
):
    """
    Get appropriate transcription provider based on config.

    Args:
        use_local: If True, use faster-whisper (local). If False, use Groq API.
        whisper_model: Model size for faster-whisper (tiny, base, small, medium, large-v3).
        device: Device for faster-whisper (cpu, cuda, auto).
        groq_api_key: API key for Groq (required if use_local=False).

    Returns:
        Transcription provider instance.
    """
    global _local_transcriber, _groq_transcriber

    if use_local:
        if _local_transcriber is None or _local_transcriber.whisper_model != whisper_model or _local_transcriber.device != device:
            _local_transcriber = LocalTranscriptionProvider(whisper_model=whisper_model, device=device)
        return _local_transcriber
    else:
        if _groq_transcriber is None or groq_api_key:
            _groq_transcriber = GroqTranscriptionProvider(api_key=groq_api_key)
        return _groq_transcriber
