"""Module for loading configuration from settings.ini."""

import configparser
from pathlib import Path
from typing import Optional


class ConfigLoader:
    """Class for loading and managing configuration settings."""

    def __init__(self, config_path: str = "config/settings.ini"):
        """Initialize the ConfigLoader.

        Args:
            config_path (str, optional): Path to the settings.ini file.
                Defaults to "config/settings.ini".
        """
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        
        # Create config file with OpenAI section if it doesn't exist
        if not self.config_path.exists():
            self._create_default_config()
        
        self.config.read(self.config_path)
        
        # Ensure OpenAI section exists
        if 'OpenAI' not in self.config:
            self.config['OpenAI'] = {'api_key': ''}
            self._save_config()

    def get_openai_key(self) -> Optional[str]:
        """Get the OpenAI API key from the configuration.

        Returns:
            Optional[str]: The API key if set, None otherwise.

        Raises:
            Exception: If the OpenAI section is missing from the config.
        """
        try:
            api_key = self.config.get('OpenAI', 'api_key', fallback=None)
            if not api_key:
                print("Warning: OpenAI API key not found in settings.ini")
            return api_key
        except configparser.Error as e:
            raise Exception(f"Failed to read OpenAI API key from config: {e}")

    def set_openai_key(self, api_key: str) -> None:
        """Set the OpenAI API key in the configuration.

        Args:
            api_key (str): The API key to set.

        Raises:
            Exception: If failed to save the configuration.
        """
        if 'OpenAI' not in self.config:
            self.config['OpenAI'] = {}
        self.config['OpenAI']['api_key'] = api_key
        self._save_config()

    def _create_default_config(self) -> None:
        """Create a default configuration file if it doesn't exist."""
        self.config['OpenAI'] = {'api_key': ''}
        self._save_config()

    def _save_config(self) -> None:
        """Save the current configuration to file.

        Raises:
            Exception: If failed to save the configuration.
        """
        try:
            # Ensure the directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the config file
            with open(self.config_path, 'w') as config_file:
                self.config.write(config_file)
        except Exception as e:
            raise Exception(f"Failed to save configuration: {e}")
