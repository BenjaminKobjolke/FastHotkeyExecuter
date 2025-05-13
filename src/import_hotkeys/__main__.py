#!/usr/bin/env python3
"""Script for importing hotkeys from web pages."""

import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup

from src.import_hotkeys.web.ChromeWebCrawler import ChromeWebCrawler
from src.utils.StringUtils import StringUtils
from src.import_hotkeys.web.content_cleaner import ContentCleaner
from src.import_hotkeys.openai.api_client import OpenAIClient
from src.import_hotkeys.openai.prompt_builder import PromptBuilder
from src.import_hotkeys.data.config_loader import ConfigLoader
from src.import_hotkeys.data.json_writer import JsonWriter


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments and prompt for missing ones.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Import hotkeys from a webpage and save them as JSON.'
    )
    parser.add_argument(
        '--name',
        help='Name of the application (used for directory name)'
    )
    parser.add_argument(
        '--url',
        help='URL of the webpage containing hotkeys'
    )
    parser.add_argument(
        '--filename',
        help='Name for the output JSON file (defaults to app name)'
    )
    parser.add_argument(
        '--prefix',
        help='Prefix to add to all hotkey names'
    )
    parser.add_argument(
        '--window-title',
        help='Window title pattern to match'
    )
    
    # Parse known args first to handle optional arguments
    args, _ = parser.parse_known_args()
    
    # Prompt for missing arguments
    if not args.name:
        args.name = input("Please enter the application name (task name found in taskmanager, without extension): ")
    if not args.url:
        args.url = input("Please enter the URL containing hotkeys: ")
    if args.prefix is None:  # Note: using None check since empty string is valid
        args.prefix = input("Enter prefix for hotkey names (optional, press Enter to skip): ").strip()
    if args.window_title is None:
        args.window_title = input("Enter window title pattern (optional, press Enter to skip): ").strip()
    
    return args


def main() -> None:
    """Main function to run the hotkey import process."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Construct output path and check for file existence early
        app_dir = Path('data/hotkeys') / args.name
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Use provided filename or app name as default
        filename = args.filename if args.filename else args.name
            
        while True:
            output_path = app_dir / f"{filename}.json"
            if output_path.exists():
                if args.filename:
                    # If user provided a filename and it exists, ask to override or exit
                    response = input(f"File {output_path} already exists. Override? (y/n): ").strip()
                    if not response or response.lower() != 'y':
                        print("Operation cancelled")
                        sys.exit(0)
                    break
                else:
                    # If no filename was provided and default exists, ask to override or provide new name
                    response = input(f"File {output_path} already exists. Override? (y/n): ").strip()
                    if response.lower() == 'y':
                        break
                    new_filename = input("Enter new filename (without .json): ").strip()
                    if new_filename:
                        filename = new_filename
                    else:
                        print("Operation cancelled")
                        sys.exit(0)
            else:
                break

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
        
        # Save raw HTML content with the same filename identifier
        cleaner.save_html(result['text'], args.name, filename)
        
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

        # Save results with metadata
        print("Saving hotkeys")
        output_path = json_writer.save_hotkeys(
            args.name, 
            hotkeys, 
            filename=filename, 
            url=args.url,
            prefix=args.prefix,
            window_title=args.window_title
        )
        print(f"Hotkeys saved to: {output_path}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
