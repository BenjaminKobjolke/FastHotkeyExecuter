"""Module for cleaning and extracting relevant content from webpage HTML."""

from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional
from utils.FileUtils import FileUtils


class ContentCleaner:
    """Class for cleaning and extracting relevant content from HTML."""

    def __init__(self):
        """Initialize ContentCleaner."""
        self.tmp_dir = Path('tmp/html')
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def save_html(self, html: str, name: str, filename: str = None) -> None:
        """Save HTML content to tmp/html directory.
        
        Args:
            html (str): The HTML content to save
            name (str): The name of the application
            filename (str, optional): Additional identifier for the file name
        """
        # Clean names for filename
        clean_name = name.lower().replace(' ', '_')
        clean_filename = filename.lower().replace(' ', '_') if filename else ""
        
        # Save HTML in tmp directory
        html_path = self.tmp_dir / f"{clean_name}_{clean_filename}_source.html" if clean_filename else self.tmp_dir / f"{clean_name}_source.html"
        html_path.write_text(html, encoding='utf-8')
        print(f"Saved HTML content to: {html_path}")

    def clean(self, soup: Optional[BeautifulSoup], name: str = None) -> str:
        """Clean HTML content.

        Args:
            soup (Optional[BeautifulSoup]): BeautifulSoup object to clean.
                If None, returns empty string.
            name (str, optional): Name used for logging. Defaults to None.

        Returns:
            str: Cleaned content.
        """
        if not soup:
            return ""

        # Extract text content
        text = soup.get_text(separator='\n', strip=True)

        # Clean up extra whitespace and empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(lines)

        return cleaned_text
