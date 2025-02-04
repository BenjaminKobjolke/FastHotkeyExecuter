"""OpenAI module for extracting hotkeys from webpage content."""

from .api_client import OpenAIClient
from .prompt_builder import PromptBuilder

__all__ = ['OpenAIClient', 'PromptBuilder']
