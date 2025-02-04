"""Module for building prompts for OpenAI API interactions."""

from typing import Optional


class PromptBuilder:
    """Class for building prompts for OpenAI API interactions."""

    @staticmethod
    def build_extraction_prompt(content: str, platform: str = "windows") -> str:
        """Build a prompt for extracting hotkeys from content.

        Args:
            content (str): The content to extract hotkeys from.
            platform (str, optional): The platform to extract hotkeys for.
                Defaults to "windows".

        Returns:
            str: The formatted prompt for the OpenAI API.
        """
        # Remove any potential null bytes or other invalid characters
        cleaned_content = content.replace('\x00', '').strip()

        # Build the prompt with clear instructions
        prompt = (
            f"Extract {platform} keyboard shortcuts from the following content. "
            "Format the response as a JSON object with a 'hotkeys' array. "
            "Each item in the array should have 'name' (description of the action) "
            "and 'hotkey' (the keyboard shortcut) properties. "
            "Format hotkeys in lowercase with '+' between keys (e.g., 'ctrl+shift+p'). "
            "For mouse actions, use 'wheelup' for scroll up and 'wheeldown' for scroll down. "
            f"Only include {platform} shortcuts.\n\n{cleaned_content}"
        )

        return prompt

    @staticmethod
    def clean_hotkey(hotkey: str) -> str:
        """Clean and standardize a hotkey string.

        Args:
            hotkey (str): The hotkey string to clean.

        Returns:
            str: The cleaned hotkey string.
        """
        # Convert to lowercase
        hotkey = hotkey.lower()

        # Replace common variations
        replacements = {
            'control': 'ctrl',
            'command': 'ctrl',  # For Windows
            'cmd': 'ctrl',     # For Windows
            'return': 'enter',
            'plus': '+',
            ' + ': '+',
            ' +': '+',
            '+ ': '+',
            'scroll up': 'wheelup',
            'scroll down': 'wheeldown',
            'wheel up': 'wheelup',
            'wheel down': 'wheeldown',
            'mouse wheel up': 'wheelup',
            'mouse wheel down': 'wheeldown',
        }

        for old, new in replacements.items():
            hotkey = hotkey.replace(old, new)

        # Remove any remaining whitespace
        hotkey = hotkey.strip()

        return hotkey
