"""Text-to-speech provider using Kokoro."""

import os
import time
from pathlib import Path

import soundfile as sf
import torch
from loguru import logger


class KokoroTTSProvider:
    """
    Local TTS using Kokoro.

    Generates speech audio files from text.
    """

    def __init__(self, voice: str = "af_heart", lang_code: str = "b"):
        self.voice = voice
        self.lang_code = lang_code
        self._pipeline = None

    def _load_pipeline(self):
        """Lazy load the Kokoro pipeline."""
        if self._pipeline is None:
            try:
                from kokoro import KPipeline

                self._pipeline = KPipeline(lang_code=self.lang_code)
            except ImportError as e:
                raise RuntimeError(f"kokoro not installed: {e}") from e
        return self._pipeline

    def speak(self, text: str, output_dir: Path | None = None) -> Path:
        """
        Generate speech from text.

        Args:
            text: Text to synthesize.
            output_dir: Output directory (defaults to workspace/media/tts).

        Returns:
            Path to generated WAV file.

        Raises:
            RuntimeError: If kokoro is not installed or generation fails.
        """
        if not text or not text.strip():
            raise ValueError("text cannot be empty")

        pipeline = self._load_pipeline()

        if output_dir is None:
            output_dir = Path.home() / ".mybot" / "workspace" / "media" / "tts"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = int(time.time())
        random_hex = os.urandom(4).hex()
        output_path = output_dir / f"tts_{timestamp}_{random_hex}.wav"

        logger.info(f"Generating TTS: '{text[:50]}...' → {output_path.name}")

        try:
            generator = pipeline(text, voice=self.voice)

            audio_chunks = []
            for gs, ps, audio in generator:
                audio_chunks.append(audio)

            if not audio_chunks:
                raise RuntimeError("No audio generated")

            if len(audio_chunks) > 1:
                final_audio = torch.cat(audio_chunks, dim=0)
            else:
                final_audio = audio_chunks[0]

            audio_np = final_audio.cpu().numpy()
            sf.write(str(output_path), audio_np, 24000)

            logger.info(f"TTS generated: {output_path}")
            return output_path

        except Exception as e:
            raise RuntimeError(f"TTS generation failed: {e}") from e


_tts_provider: KokoroTTSProvider | None = None


def get_tts_provider(voice: str = "af_heart", lang_code: str = "b") -> KokoroTTSProvider:
    """
    Get singleton TTS provider instance.

    Args:
        voice: Voice preset.
        lang_code: Language code.

    Returns:
        KokoroTTSProvider instance.
    """
    global _tts_provider

    if _tts_provider is None or _tts_provider.voice != voice or _tts_provider.lang_code != lang_code:
        _tts_provider = KokoroTTSProvider(voice=voice, lang_code=lang_code)

    return _tts_provider
