"""Module for fetching webpage content using Selenium."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from typing import Optional, Tuple
from pathlib import Path
import time
import os


class WebpageFetcher:
    """Class for fetching and parsing webpage content using Selenium."""

    def __init__(self, timeout: int = 30):
        """Initialize the WebpageFetcher with Chrome WebDriver.

        Args:
            timeout (int): Page load timeout in seconds. Defaults to 30.
        """
        self.timeout = timeout
        self.driver = None

    def _setup_driver(self) -> None:
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        # Visible browser (removed headless mode)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        # Install and setup ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout)

    def fetch(self, url: str, name: str) -> Tuple[str, Optional[BeautifulSoup]]:
        """Fetch webpage content from the given URL using Selenium.

        Args:
            url (str): The URL to fetch content from.

        Returns:
            Tuple[str, Optional[BeautifulSoup]]: A tuple containing the raw HTML content
                and BeautifulSoup object if parsing was successful.

        Raises:
            Exception: If the page fails to load or other errors occur.
        """
        try:
            if not self.driver:
                self._setup_driver()

            print("Loading page with Chrome WebDriver...")
            self.driver.get(url)
            
            # Wait for the page to load and stabilize
            time.sleep(5)  # Give JavaScript some time to execute
            
            # Get the page source
            html_content = self.driver.page_source
            
            # Save HTML content to tmp/html directory
            tmp_dir = Path('tmp/html')
            tmp_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename and save HTML
            clean_name = name.lower().replace(' ', '_')
            html_path = tmp_dir / f"{clean_name}.html"
            html_path.write_text(html_content, encoding='utf-8')
            print(f"Saved HTML content to: {html_path}")
            
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                return html_content, soup
            except Exception as e:
                print(f"Warning: Failed to parse HTML content: {e}")
                return html_content, None

        except TimeoutException:
            raise Exception("Page load timed out")
        except Exception as e:
            raise Exception(f"Failed to fetch webpage: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

    def __del__(self):
        """Ensure the WebDriver is closed."""
        if self.driver:
            self.driver.quit()
