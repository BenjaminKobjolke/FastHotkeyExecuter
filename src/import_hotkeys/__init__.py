"""Import hotkeys package for extracting keyboard shortcuts from web pages."""

from .web.webpage_fetcher import WebpageFetcher
from .web.content_cleaner import ContentCleaner
from .openai.api_client import OpenAIClient
from .openai.prompt_builder import PromptBuilder
from .data.config_loader import ConfigLoader
from .data.json_writer import JsonWriter

__all__ = [
    'WebpageFetcher',
    'ContentCleaner',
    'OpenAIClient',
    'PromptBuilder',
    'ConfigLoader',
    'JsonWriter'
]
