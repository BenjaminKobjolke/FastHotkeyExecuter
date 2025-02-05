"""Module for interacting with OpenAI API to extract hotkeys."""

from openai import OpenAI
from typing import List, Dict, Any
from pathlib import Path
import json
import os


class OpenAIClient:
    """Class for handling OpenAI API interactions."""

    def __init__(self, api_key: str):
        """Initialize the OpenAI client.

        Args:
            api_key (str): OpenAI API key.
        """
        self.client = OpenAI(api_key=api_key)

    def extract_hotkeys(self, content: str, name: str) -> List[Dict[str, str]]:
        """Extract hotkeys from content using OpenAI API.

        Args:
            content (str): The webpage content to analyze.
            name (str): Name of the application/context for the hotkeys.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing hotkey information.
                Each dictionary has 'name' and 'hotkey' keys.

        Raises:
            Exception: If API call fails or response is invalid.
        """
        try:
            # Read prompts from config files
            config_dir = Path('config')
            system_prompt_path = config_dir / 'ai_system_prompt.txt'
            user_prompt_path = config_dir / 'ai_user_prompt.txt'

            if not system_prompt_path.exists() or not user_prompt_path.exists():
                raise Exception("Prompt configuration files not found")

            system_prompt = system_prompt_path.read_text(encoding='utf-8').strip()
            user_prompt = user_prompt_path.read_text(encoding='utf-8').strip()

            # Format user prompt with content
            formatted_user_prompt = user_prompt.format(content=content)

            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                max_tokens=16000,  # Maximum tokens for GPT-4-0125-preview
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": formatted_user_prompt
                    }
                ]
            )

            # Extract the JSON content from the response
            result = response.choices[0].message.content
            if not result:
                print("Empty response from OpenAI API")
                raise Exception("Empty response from OpenAI API")

            # Save raw OpenAI response as both txt and json
            tmp_dir = Path('tmp/ai')
            tmp_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename and save raw response as txt
            clean_name = name.lower().replace(' ', '_')
            txt_path = tmp_dir / f"{clean_name}_response.txt"
            txt_path.write_text(result, encoding='utf-8')
            print(f"Saved raw OpenAI response to: {txt_path}")
            
            # Also save as JSON for convenience
            json_path = tmp_dir / f"{clean_name}_response.json"
            json_path.write_text(result, encoding='utf-8')
            print(f"Saved OpenAI response as JSON: {json_path}")

            # Parse the JSON string into a Python object
            try:
                data = json.loads(result)
                # Expect a 'hotkeys' array in the response
                if not isinstance(data, dict) or 'hotkeys' not in data:
                    raise Exception("Invalid response format: missing 'hotkeys' array")
                return data['hotkeys']
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse OpenAI response as JSON: {e}")

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def __del__(self):
        """Cleanup method for the OpenAI client."""
        # OpenAI client doesn't require explicit cleanup
        pass
