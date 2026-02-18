"""Media encoding utilities for vision/audio-capable models."""

import asyncio
import base64
import mimetypes
import shutil
import tempfile
from pathlib import Path

import httpx

IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp3", "audio/webm", "audio/x-wav"}
VIDEO_TYPES = {"video/mp4", "video/quicktime", "video/webm"}


def is_vision_capable(model: str) -> bool:
    """Check if model supports vision input via LiteLLM."""
    try:
        import litellm

        if hasattr(litellm, "supports_vision"):
            return litellm.supports_vision(model)
        return False
    except Exception:
        return False


def is_audio_capable(model: str) -> bool:
    """Check if model supports audio input via LiteLLM."""
    try:
        import litellm

        if hasattr(litellm, "supports_audio_input"):
            return litellm.supports_audio_input(model)
        return False
    except Exception:
        return False


def _normalize_mime(content_type: str | None) -> str:
    """Normalize Content-Type header, stripping charset and params."""
    if not content_type:
        return ""
    return content_type.split(";")[0].strip().lower()


def encode_image_file(path: str) -> str | None:
    """Encode local image as base64 data URI."""
    p = Path(path)
    if not p.is_file():
        return None

    mime, _ = mimetypes.guess_type(path)
    if mime not in IMAGE_TYPES:
        return None

    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


async def encode_image_url(url: str, timeout: float = 30.0) -> str | None:
    """Download image from URL and encode as base64 data URI."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
            r = await client.get(url)
            r.raise_for_status()

        content = r.content
        raw_mime = r.headers.get("content-type")
        mime = _normalize_mime(raw_mime)

        if not mime or mime not in IMAGE_TYPES:
            mime, _ = mimetypes.guess_type(url)
            if mime not in IMAGE_TYPES:
                mime = "image/jpeg"

        b64 = base64.b64encode(content).decode()
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def encode_audio_file(path: str) -> tuple[str, str] | None:
    """Encode local audio as base64. Returns (base64, format) - NOT a data URI."""
    p = Path(path)
    if not p.is_file():
        return None

    mime, _ = mimetypes.guess_type(path)
    if mime not in AUDIO_TYPES:
        return None

    b64 = base64.b64encode(p.read_bytes()).decode()

    format_map = {
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/ogg": "ogg",
        "audio/webm": "webm",
    }
    return b64, format_map.get(mime, "wav")


async def encode_audio_url(url: str, timeout: float = 30.0) -> tuple[str, str] | None:
    """Download audio from URL and encode as base64. Returns (base64, format)."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
            r = await client.get(url)
            r.raise_for_status()

        content = r.content
        raw_mime = r.headers.get("content-type")
        mime = _normalize_mime(raw_mime)

        if mime not in AUDIO_TYPES:
            mime, _ = mimetypes.guess_type(url)

        format_map = {
            "audio/mpeg": "mp3",
            "audio/wav": "wav",
            "audio/ogg": "ogg",
            "audio/webm": "webm",
        }

        b64 = base64.b64encode(content).decode()
        return b64, format_map.get(mime, "wav")
    except Exception:
        return None


def _get_ffmpeg_path() -> str | None:
    """Find ffmpeg binary path. Returns None if not available."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    for path in ["/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
        if Path(path).exists():
            return path
    return None


def _get_ffprobe_path() -> str | None:
    """Get ffprobe binary path."""
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        return ffprobe
    for path in ["/usr/bin/ffprobe", "/usr/local/bin/ffprobe"]:
        if Path(path).exists():
            return path
    return None


async def _get_video_duration(ffmpeg_path: str, video_path: str) -> float | None:
    """Get video duration in seconds using ffprobe."""
    ffprobe = _get_ffprobe_path()
    if not ffprobe:
        ffprobe = ffmpeg_path.replace("ffmpeg", "ffprobe")

    try:
        cmd = [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            video_path,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        if proc.returncode == 0:
            return float(stdout.decode().strip())
    except Exception:
        pass
    return None


async def _extract_single_frame(ffmpeg_path: str, video_path: str, timestamp: float) -> str | None:
    """Extract a single frame at the given timestamp."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name

        cmd = [
            ffmpeg_path,
            "-ss",
            str(timestamp),
            "-i",
            video_path,
            "-vframes",
            "1",
            "-q:v",
            "2",
            "-y",
            tmp_path,
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        if Path(tmp_path).exists():
            with open(tmp_path, "rb") as f:
                data = f.read()
            Path(tmp_path).unlink()

            b64 = base64.b64encode(data).decode()
            return f"data:image/jpeg;base64,{b64}"

    except Exception:
        pass

    return None


async def extract_video_frames(path: str, max_frames: int = 16) -> list[str]:
    """Extract frames from video as base64 data URIs.

    Uses head/tail trimming and increasing frame budget per the video frame extraction plan.
    """
    import math

    ffmpeg_path = _get_ffmpeg_path()
    if not ffmpeg_path:
        return []

    video_path = Path(path)
    if not video_path.exists():
        return []

    duration = await _get_video_duration(ffmpeg_path, str(video_path))
    if not duration or duration <= 0:
        return []

    # Head trim: remove startup junk (camera shake, black frames, mic click)
    head_trim = min(0.25, duration * 0.10)

    # Tail trim: remove outro junk (fades, credits, silence)
    tail_trim = min(0.5, duration * 0.15)

    # Usable window
    usable_duration = max(0.0, duration - head_trim - tail_trim)

    # Frame budget: increasing with duration, capped at max_frames
    if usable_duration <= 0:
        frames_to_extract = 1
    else:
        frames_to_extract = math.ceil(usable_duration / 2.0)
        frames_to_extract = max(1, min(max_frames, frames_to_extract))

    # Sample times: distribute frames evenly within usable window
    if frames_to_extract == 1 or usable_duration <= 0:
        timestamps = [head_trim + usable_duration / 2]
    else:
        step = usable_duration / (frames_to_extract + 1)
        timestamps = [head_trim + step * (i + 1) for i in range(frames_to_extract)]

    frames: list[str] = []

    for ts in timestamps:
        frame_data = await _extract_single_frame(ffmpeg_path, str(video_path), ts)
        if frame_data:
            frames.append(frame_data)

    return frames


async def _video_has_audio(ffmpeg_path: str, video_path: str) -> bool:
    """Check if video has an audio stream."""
    ffprobe = _get_ffprobe_path()
    if not ffprobe:
        ffprobe = ffmpeg_path.replace("ffmpeg", "ffprobe")

    try:
        cmd = [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "csv=p=0",
            video_path,
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()

        return bool(stdout.decode().strip())

    except Exception:
        return False


async def extract_video_audio(path: str) -> tuple[str, str] | None:
    """Extract audio track from video as base64. Returns (base64, format)."""
    ffmpeg_path = _get_ffmpeg_path()
    if not ffmpeg_path:
        return None

    video_path = Path(path)
    if not video_path.exists():
        return None

    has_audio = await _video_has_audio(ffmpeg_path, str(video_path))
    if not has_audio:
        return None

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        cmd = [
            ffmpeg_path,
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            "-y",
            tmp_path,
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        if Path(tmp_path).exists():
            with open(tmp_path, "rb") as f:
                data = f.read()
            Path(tmp_path).unlink()

            b64 = base64.b64encode(data).decode()
            return b64, "wav"

    except Exception:
        pass

    return None


async def _download_video_to_temp(url: str) -> str | None:
    """Download video URL to temporary file."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
            r = await client.get(url)
            r.raise_for_status()

        content = r.content
        ext = ".mp4"
        cd = r.headers.get("content-disposition", "")
        if "filename=" in cd:
            import re

            match = re.search(r'filename="?([^";\s]+)"?', cd)
            if match:
                ext = Path(match.group(1)).suffix

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(content)
            return tmp.name

    except Exception:
        return None


async def process_video(
    path_or_url: str,
    max_frames: int = 16,
) -> tuple[list[str], tuple[str, str] | None]:
    """Process video into frames and audio."""
    if path_or_url.startswith(("http://", "https://")):
        local_path = await _download_video_to_temp(path_or_url)
        if not local_path:
            return [], None
    else:
        local_path = path_or_url

    try:
        frames = await extract_video_frames(local_path, max_frames)
        audio = await extract_video_audio(local_path)
        return frames, audio
    finally:
        if path_or_url.startswith(("http://", "https://")) and local_path:
            try:
                Path(local_path).unlink()
            except Exception:
                pass
