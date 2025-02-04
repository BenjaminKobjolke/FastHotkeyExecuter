"""Module for interacting with OpenAI API to extract hotkeys."""

from openai import OpenAI
from typing import List, Dict, Any
from pathlib import Path
import json


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

        Returns:
            List[Dict[str, str]]: List of dictionaries containing hotkey information.
                Each dictionary has 'name' and 'hotkey' keys.

        Raises:
            Exception: If API call fails or response is invalid.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a hotkey extraction specialist. Extract Windows "
                            "keyboard shortcuts from the provided content and return them "
                            "in a JSON format with an array of objects, each containing "
                            "'name' (description of the action) and 'hotkey' (the keyboard "
                            "shortcut) properties. Format hotkeys using lowercase with '+' "
                            "between keys (e.g., 'ctrl+shift+p'). Include only Windows "
                            "shortcuts."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            "Extract Windows keyboard shortcuts from this content and "
                            f"return them in JSON format:\n\n{content}"
                        )
                    }
                ]
            )

            # Extract the JSON content from the response
            result = response.choices[0].message.content
            if not result:
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
