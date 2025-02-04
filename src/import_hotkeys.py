#!/usr/bin/env python3
"""Script for importing hotkeys from web pages."""

import argparse
import sys
from pathlib import Path

from import_hotkeys.web.webpage_fetcher import WebpageFetcher
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

        fetcher = WebpageFetcher()
        cleaner = ContentCleaner()
        prompt_builder = PromptBuilder()
        openai_client = OpenAIClient(api_key)
        json_writer = JsonWriter()

        # Fetch and process webpage
        print(f"Fetching webpage: {args.url}")
        html_content, soup = fetcher.fetch(args.url, args.name)
        if not soup:
            print("Warning: Failed to parse HTML, using raw content")
            cleaned_content = cleaner.clean(soup)
        else:
            print("Extracting relevant sections")
            cleaned_content = cleaner.extract_hotkey_sections(soup)
            if not cleaned_content:
                print("Warning: No relevant sections found, using cleaned content")
                cleaned_content = cleaner.clean(soup)

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
