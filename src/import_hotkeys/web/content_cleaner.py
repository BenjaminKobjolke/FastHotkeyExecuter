"""Module for cleaning and extracting relevant content from webpage HTML."""

from bs4 import BeautifulSoup
from typing import Optional


class ContentCleaner:
    """Class for cleaning and extracting relevant content from HTML."""

    @staticmethod
    def clean(soup: Optional[BeautifulSoup]) -> str:
        """Clean and extract body content from BeautifulSoup object.

        Args:
            soup (Optional[BeautifulSoup]): BeautifulSoup object to clean.
                If None, returns empty string.

        Returns:
            str: Cleaned content from the body tag.
        """
        if not soup:
            return ""

        # Find the body tag
        body = soup.find('body')
        if not body:
            return ""

        # Remove script and style elements from body
        for element in body(['script', 'style', 'meta', 'link', 'noscript', 'header', 'footer', 'nav']):
            element.decompose()

        # Extract text content from body only
        text = body.get_text(separator='\n', strip=True)

        # Clean up extra whitespace and empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(lines)

        return cleaned_text

    @staticmethod
    def extract_hotkey_sections(soup: Optional[BeautifulSoup]) -> str:
        """Extract sections likely to contain hotkey information.

        Args:
            soup (Optional[BeautifulSoup]): BeautifulSoup object to extract from.
                If None, returns empty string.

        Returns:
            str: Extracted content focusing on sections with hotkey information.
        """
        if not soup:
            return ""

        relevant_content = []

        # Find the body tag
        body = soup.find('body')
        if not body:
            return ""

        # Remove unwanted elements from body
        for element in body(['script', 'style', 'meta', 'link', 'noscript', 'header', 'footer', 'nav']):
            element.decompose()

        # Look for tables that might contain hotkeys
        tables = body.find_all('table')
        for table in tables:
            if any(keyword in table.get_text().lower() 
                  for keyword in ['shortcut', 'hotkey', 'keyboard', 'key']):
                relevant_content.append(table.get_text(separator='\n', strip=True))

        # Look for lists that might contain hotkeys
        lists = body.find_all(['ul', 'ol'])
        for list_elem in lists:
            if any(keyword in list_elem.get_text().lower() 
                  for keyword in ['shortcut', 'hotkey', 'keyboard', 'key']):
                relevant_content.append(list_elem.get_text(separator='\n', strip=True))

        # Look for sections with relevant headers
        headers = body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for header in headers:
            if any(keyword in header.get_text().lower() 
                  for keyword in ['shortcut', 'hotkey', 'keyboard', 'key']):
                # Get the next sibling elements until the next header
                current = header.find_next_sibling()
                while current and current.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if current.name in ['p', 'div', 'ul', 'ol', 'table']:
                        relevant_content.append(current.get_text(separator='\n', strip=True))
                    current = current.find_next_sibling()

        return '\n\n'.join(relevant_content)
