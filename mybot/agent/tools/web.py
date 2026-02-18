"""Web tools: web_search, image_search, video_search, news_search, books_search, web_fetch."""

import asyncio
import html
import json
import re
from typing import Any
from urllib.parse import urlparse

import httpx
from ddgs import DDGS

from mybot.agent.tools.base import Tool

# Shared constants
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36"
MAX_REDIRECTS = 5  # Limit redirects to prevent DoS attacks


def _strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def _normalize(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _validate_url(url: str) -> tuple[bool, str]:
    """Validate URL: must be http(s) with valid domain."""
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False, f"Only http/https allowed, got '{p.scheme or 'none'}'"
        if not p.netloc:
            return False, "Missing domain"
        return True, ""
    except Exception as e:
        return False, str(e)


class WebSearchTool(Tool):
    """Search the web using DDGS text search."""

    name = "web_search"
    description = "Search the web for text results. Returns titles, URLs, and snippets."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "count": {"type": "integer", "description": "Max results (1-10)", "minimum": 1, "maximum": 10},
            "region": {"type": "string", "description": "Region (us-en, uk-en, ru-ru, etc.)"},
            "safesearch": {"type": "string", "enum": ["on", "moderate", "off"], "default": "moderate"},
            "timelimit": {"type": "string", "description": "Time limit (d, w, m, y)"},
        },
        "required": ["query"],
    }

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        try:
            n = min(count or self.max_results, 10)
            results = await asyncio.to_thread(
                lambda: DDGS().text(query, max_results=n, **{k: v for k, v in kwargs.items() if v})
            )
            if not results:
                return f"No results for: {query}"

            lines = [f"Web results for: {query}\n"]
            for i, item in enumerate(results[:n], 1):
                lines.append(f"{i}. {item.get('title', '')}\n   {item.get('href', '')}")
                if body := item.get("body"):
                    lines.append(f"   {body}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class ImageSearchTool(Tool):
    """Search for images using DDGS."""

    name = "image_search"
    description = "Search for images. Returns image URLs, thumbnails, and sources."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Image search query"},
            "count": {"type": "integer", "description": "Max results (1-10)", "minimum": 1, "maximum": 10},
            "region": {"type": "string", "default": "us-en"},
            "safesearch": {"type": "string", "enum": ["on", "moderate", "off"], "default": "moderate"},
            "size": {"type": "string", "enum": ["Small", "Medium", "Large", "Wallpaper"]},
            "color": {"type": "string"},
            "type_image": {"type": "string", "enum": ["photo", "clipart", "gif", "transparent", "line"]},
        },
        "required": ["query"],
    }

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        try:
            n = min(count or self.max_results, 10)
            results = await asyncio.to_thread(
                lambda: DDGS().images(query, max_results=n, **{k: v for k, v in kwargs.items() if v})
            )
            if not results:
                return f"No image results for: {query}"

            lines = [f"Image results for: {query}\n"]
            for i, item in enumerate(results[:n], 1):
                lines.append(f"{i}. {item.get('title', '')}\n   {item.get('url', '')}")
                lines.append(f"   Thumbnail: {item.get('thumbnail', '')}")
                lines.append(f"   Source: {item.get('source', '')}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class VideoSearchTool(Tool):
    """Search for videos using DDGS."""

    name = "video_search"
    description = "Search for videos. Returns video URLs, descriptions, and duration."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Video search query"},
            "count": {"type": "integer", "description": "Max results (1-10)", "minimum": 1, "maximum": 10},
            "region": {"type": "string", "default": "us-en"},
            "safesearch": {"type": "string", "enum": ["on", "moderate", "off"], "default": "moderate"},
            "timelimit": {"type": "string", "enum": ["d", "w", "m"]},
            "resolution": {"type": "string", "enum": ["high", "standard"]},
            "duration": {"type": "string", "enum": ["short", "medium", "long"]},
        },
        "required": ["query"],
    }

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        try:
            n = min(count or self.max_results, 10)
            results = await asyncio.to_thread(
                lambda: DDGS().videos(query, max_results=n, **{k: v for k, v in kwargs.items() if v})
            )
            if not results:
                return f"No video results for: {query}"

            lines = [f"Video results for: {query}\n"]
            for i, item in enumerate(results[:n], 1):
                lines.append(f"{i}. {item.get('title', '')}\n   {item.get('content', '')}")
                if dur := item.get("duration"):
                    lines.append(f"   Duration: {dur}")
                if pub := item.get("publisher"):
                    lines.append(f"   Publisher: {pub}")
                if url := item.get("content"):
                    lines.append(f"   URL: {url}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class NewsSearchTool(Tool):
    """Search for news using DDGS."""

    name = "news_search"
    description = "Search for news articles. Returns titles, URLs, sources, and dates."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "News search query"},
            "count": {"type": "integer", "description": "Max results (1-10)", "minimum": 1, "maximum": 10},
            "region": {"type": "string", "default": "us-en"},
            "safesearch": {"type": "string", "enum": ["on", "moderate", "off"], "default": "moderate"},
            "timelimit": {"type": "string", "enum": ["d", "w", "m"]},
        },
        "required": ["query"],
    }

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        try:
            n = min(count or self.max_results, 10)
            results = await asyncio.to_thread(
                lambda: DDGS().news(query, max_results=n, **{k: v for k, v in kwargs.items() if v})
            )
            if not results:
                return f"No news results for: {query}"

            lines = [f"News results for: {query}\n"]
            for i, item in enumerate(results[:n], 1):
                lines.append(f"{i}. {item.get('title', '')}\n   {item.get('url', '')}")
                if date := item.get("date"):
                    lines.append(f"   Date: {date}")
                if body := item.get("body"):
                    lines.append(f"   {body}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class BooksSearchTool(Tool):
    """Search for books using DDGS."""

    name = "books_search"
    description = "Search for books. Returns titles, authors, publishers, and download links."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Book search query"},
            "count": {"type": "integer", "description": "Max results (1-10)", "minimum": 1, "maximum": 10},
        },
        "required": ["query"],
    }

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        try:
            n = min(count or self.max_results, 10)
            results = await asyncio.to_thread(
                lambda: DDGS().books(query, max_results=n)
            )
            if not results:
                return f"No book results for: {query}"

            lines = [f"Book results for: {query}\n"]
            for i, item in enumerate(results[:n], 1):
                lines.append(f"{i}. {item.get('title', '')}")
                if author := item.get("author"):
                    lines.append(f"   Author: {author}")
                if pub := item.get("publisher"):
                    lines.append(f"   Publisher: {pub}")
                if info := item.get("info"):
                    lines.append(f"   Info: {info}")
                lines.append(f"   URL: {item.get('url', '')}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class WebFetchTool(Tool):
    """Fetch and extract content from a URL using Readability."""

    name = "web_fetch"
    description = "Fetch URL and extract readable content (HTML → markdown/text)."
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "URL to fetch"},
            "extractMode": {"type": "string", "enum": ["markdown", "text"], "default": "markdown"},
            "maxChars": {"type": "integer", "minimum": 100},
        },
        "required": ["url"],
    }

    def __init__(self, max_chars: int = 50000):
        self.max_chars = max_chars

    async def execute(
        self, url: str, extractMode: str = "markdown", maxChars: int | None = None, **kwargs: Any
    ) -> str:
        from readability import Document

        max_chars = maxChars or self.max_chars

        # Validate URL before fetching
        is_valid, error_msg = _validate_url(url)
        if not is_valid:
            return json.dumps({"error": f"URL validation failed: {error_msg}", "url": url})

        try:
            async with httpx.AsyncClient(
                follow_redirects=True, max_redirects=MAX_REDIRECTS, timeout=30.0
            ) as client:
                r = await client.get(url, headers={"User-Agent": USER_AGENT})
                r.raise_for_status()

            ctype = r.headers.get("content-type", "")

            # JSON
            if "application/json" in ctype:
                text, extractor = json.dumps(r.json(), indent=2), "json"
            # HTML
            elif "text/html" in ctype or r.text[:256].lower().startswith(("<!doctype", "<html")):
                doc = Document(r.text)
                content = (
                    self._to_markdown(doc.summary())
                    if extractMode == "markdown"
                    else _strip_tags(doc.summary())
                )
                text = f"# {doc.title()}\n\n{content}" if doc.title() else content
                extractor = "readability"
            else:
                text, extractor = r.text, "raw"

            truncated = len(text) > max_chars
            if truncated:
                text = text[:max_chars]

            return json.dumps(
                {
                    "url": url,
                    "finalUrl": str(r.url),
                    "status": r.status_code,
                    "extractor": extractor,
                    "truncated": truncated,
                    "length": len(text),
                    "text": text,
                }
            )
        except Exception as e:
            return json.dumps({"error": str(e), "url": url})

    def _to_markdown(self, html: str) -> str:
        """Convert HTML to markdown."""
        # Convert links, headings, lists before stripping tags
        text = re.sub(
            r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>',
            lambda m: f"[{_strip_tags(m[2])}]({m[1]})",
            html,
            flags=re.I,
        )
        text = re.sub(
            r"<h([1-6])[^>]*>([\s\S]*?)</h\1>",
            lambda m: f"\n{'#' * int(m[1])} {_strip_tags(m[2])}\n",
            text,
            flags=re.I,
        )
        text = re.sub(
            r"<li[^>]*>([\s\S]*?)</li>", lambda m: f"\n- {_strip_tags(m[1])}", text, flags=re.I
        )
        text = re.sub(r"</(p|div|section|article)>", "\n\n", text, flags=re.I)
        text = re.sub(r"<(br|hr)\s*/?>", "\n", text, flags=re.I)
        return _normalize(_strip_tags(text))


class AnalyzeImageTool(Tool):
    """Download an image from URL and prepare it for vision analysis."""

    name = "analyze_image"
    description = "Download an image from URL and prepare it for vision model analysis. " \
                   "Use this to analyze images from search results or URLs."
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Image URL to analyze"},
            "question": {"type": "string", "description": "What to ask about the image"},
        },
        "required": ["url"],
    }

    async def execute(self, url: str, question: str | None = None, **kwargs: Any) -> str:
        from mybot.utils.media import encode_image_url

        data_uri = await encode_image_url(url)
        if not data_uri:
            return json.dumps({
                "error": "Failed to download image",
                "url": url,
                "hint": "The URL may be invalid or inaccessible"
            })

        return json.dumps({
            "status": "ready_for_analysis",
            "data_uri": data_uri,
            "question": question or "Describe this image in detail",
        })
