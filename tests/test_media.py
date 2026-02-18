"""Tests for media encoding utilities."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from mybot.utils.media import (
    _normalize_mime,
    encode_image_file,
    encode_audio_file,
    is_vision_capable,
    is_audio_capable,
)


class TestNormalizeMime:
    """Tests for MIME type normalization."""

    def test_normalize_mime_with_charset(self):
        """Test MIME normalization strips charset."""
        assert _normalize_mime("image/jpeg; charset=binary") == "image/jpeg"
        assert _normalize_mime("audio/mpeg; charset=utf-8") == "audio/mpeg"
        assert _normalize_mime("image/png; charset=binary") == "image/png"

    def test_normalize_mime_without_charset(self):
        """Test MIME normalization handles clean types."""
        assert _normalize_mime("image/png") == "image/png"
        assert _normalize_mime("audio/wav") == "audio/wav"

    def test_normalize_mime_empty(self):
        """Test MIME normalization handles None/empty."""
        assert _normalize_mime(None) == ""
        assert _normalize_mime("") == ""


class TestEncodeImageFile:
    """Tests for local image encoding."""

    def test_encode_image_file_invalid_path(self):
        """Test handling of non-existent file."""
        result = encode_image_file("/nonexistent/path/image.jpg")
        assert result is None

    def test_encode_image_file_unsupported_type(self):
        """Test handling of non-image file."""
        with patch("mybot.utils.media.Path") as mock_path:
            mock_p = MagicMock()
            mock_p.is_file.return_value = True
            mock_path.return_value = mock_p

            with patch("mybot.utils.media.mimetypes") as mock_mimetypes:
                mock_mimetypes.guess_type.return_value = ("text/plain", None)
                result = encode_image_file("/path/to/file.txt")
                assert result is None


class TestEncodeAudioFile:
    """Tests for local audio encoding."""

    def test_encode_audio_file_invalid_path(self):
        """Test handling of non-existent file."""
        result = encode_audio_file("/nonexistent/path/audio.mp3")
        assert result is None

    def test_encode_audio_file_unsupported_type(self):
        """Test handling of non-audio file."""
        with patch("mybot.utils.media.Path") as mock_path:
            mock_p = MagicMock()
            mock_p.is_file.return_value = True
            mock_path.return_value = mock_p

            with patch("mybot.utils.media.mimetypes") as mock_mimetypes:
                mock_mimetypes.guess_type.return_value = ("text/plain", None)
                result = encode_audio_file("/path/to/file.txt")
                assert result is None


class TestCapabilityDetection:
    """Tests for model capability detection - basic import tests."""

    def test_is_vision_capable_import(self):
        """Test that is_vision_capable can be imported and returns a bool."""
        from mybot.utils.media import is_vision_capable

        result = is_vision_capable("gpt-4o")
        assert isinstance(result, bool)

    def test_is_audio_capable_import(self):
        """Test that is_audio_capable can be imported and returns a bool."""
        from mybot.utils.media import is_audio_capable

        result = is_audio_capable("gpt-4o")
        assert isinstance(result, bool)
