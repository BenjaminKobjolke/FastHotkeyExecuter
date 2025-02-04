"""Module for writing hotkey data to JSON files."""

import json
from pathlib import Path
from typing import List, Dict, Any


class JsonWriter:
    """Class for writing hotkey data to JSON files."""

    def __init__(self, output_dir: str = "data"):
        """Initialize the JsonWriter.

        Args:
            output_dir (str, optional): Directory to write JSON files to.
                Defaults to "data".
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_hotkeys(self, name: str, hotkeys: List[Dict[str, str]]) -> str:
        """Save hotkeys to a JSON file.

        Args:
            name (str): Name of the application (used for filename).
            hotkeys (List[Dict[str, str]]): List of hotkey dictionaries to save.
                Each dictionary should have 'name' and 'hotkey' keys.

        Returns:
            str: Path to the saved JSON file.

        Raises:
            Exception: If failed to write the JSON file.
        """
        try:
            # Clean the filename
            clean_name = self._clean_filename(name)
            output_path = self.output_dir / f"{clean_name}.json"

            # Ensure the data is properly formatted
            validated_hotkeys = self._validate_hotkeys(hotkeys)

            # Write the JSON file with proper formatting
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(validated_hotkeys, f, indent=2, ensure_ascii=False)

            return str(output_path)

        except Exception as e:
            raise Exception(f"Failed to save hotkeys to JSON: {e}")

    def _clean_filename(self, name: str) -> str:
        """Clean a string to be used as a filename.

        Args:
            name (str): The filename to clean.

        Returns:
            str: The cleaned filename.
        """
        # Remove or replace invalid filename characters
        invalid_chars = '<>:"/\\|?*'
        cleaned_name = ''.join(c if c not in invalid_chars else '_' for c in name)
        return cleaned_name.lower().strip()

    def _validate_hotkeys(self, hotkeys: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Validate and clean the hotkey data.

        Args:
            hotkeys (List[Dict[str, str]]): List of hotkey dictionaries to validate.

        Returns:
            List[Dict[str, str]]: Validated and cleaned hotkey list.

        Raises:
            ValueError: If the hotkey data is invalid.
        """
        if not isinstance(hotkeys, list):
            raise ValueError("Hotkeys must be a list")

        validated = []
        for item in hotkeys:
            if not isinstance(item, dict):
                raise ValueError("Each hotkey item must be a dictionary")
            
            if 'name' not in item or 'hotkey' not in item:
                raise ValueError("Each hotkey must have 'name' and 'hotkey' keys")
            
            if not isinstance(item['name'], str) or not isinstance(item['hotkey'], str):
                raise ValueError("Hotkey name and value must be strings")

            # Clean the data
            cleaned_item = {
                'name': item['name'].strip(),
                'hotkey': item['hotkey'].strip().lower()
            }
            
            validated.append(cleaned_item)

        return validated
