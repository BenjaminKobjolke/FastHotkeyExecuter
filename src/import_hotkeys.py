#!/usr/bin/env python3
"""Script for importing hotkeys from web pages."""

import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup

from import_hotkeys.web.ChromeWebCrawler import ChromeWebCrawler
from utils.StringUtils import StringUtils
from import_hotkeys.web.content_cleaner import ContentCleaner
from import_hotkeys.openai.api_client import OpenAIClient
from import_hotkeys.openai.prompt_builder import PromptBuilder
from import_hotkeys.data.config_loader import ConfigLoader
from import_hotkeys.data.json_writer import JsonWriter


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Import hotkeys from a webpage and save them as JSON.'
    )
    parser.add_argument(
        '--name',
        required=True,
        help='Name of the application (used for output filename)'
    )
    parser.add_argument(
        '--url',
        required=True,
        help='URL of the webpage containing hotkeys'
    )
    return parser.parse_args()


def main() -> None:
    """Main function to run the hotkey import process."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Initialize components
        config_loader = ConfigLoader()
        api_key = config_loader.get_openai_key()
        if not api_key:
            print("Error: OpenAI API key not found in settings.ini")
            print("Please add your API key to the [OpenAI] section:")
            print("api_key = your_key_here")
            sys.exit(1)

        # Get Chrome driver path from settings if available
        driver_path = config_loader.get_chromium_driver_path()
        fetcher = ChromeWebCrawler(driver_path)  # driver_path is optional
        cleaner = ContentCleaner()
        prompt_builder = PromptBuilder()
        openai_client = OpenAIClient(api_key)
        json_writer = JsonWriter()

        # Fetch and process webpage
        print(f"Fetching webpage: {args.url}")
        result = fetcher.execute(args.url)
        if not result['success']:
            print("Warning: Failed to fetch webpage content")
            sys.exit(1)
        
        # Save raw HTML content
        cleaner.save_html(result['text'], args.name)
        
        # Create BeautifulSoup object from the HTML text
        soup = BeautifulSoup(result['text'], 'html.parser')
        
        # Clean the HTML content
        print("Cleaning content")
        cleaned_content = cleaner.clean(soup, args.name)
        
        # If cleaning failed, use raw text
        if not cleaned_content:
            print("Warning: Cleaning failed, using raw content")
            cleaned_content = StringUtils.strip_html_tags(result['text'])

        # Extract hotkeys using OpenAI
        print("Extracting hotkeys using OpenAI")
        prompt = prompt_builder.build_extraction_prompt(cleaned_content)
        hotkeys = openai_client.extract_hotkeys(prompt, args.name)

        # Save results
        print("Saving hotkeys")
        output_path = json_writer.save_hotkeys(args.name, hotkeys)
        print(f"Hotkeys saved to: {output_path}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
