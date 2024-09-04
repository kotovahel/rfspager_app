import logging
import os
import time

import selenium.common

from pathlib import Path
from typing import Literal
from scraper import Scraper

base_url = 'https://rfspager.app/pager'

logger = logging.getLogger()


class App:
    browser: Literal['chrome', 'firefox']

    def __init__(self, browser: Literal['chrome', 'firefox']):
        self.browser = browser
        self.proxy = None

    def run(self):
        scraper = Scraper(self.browser, headless=True)
        scraper.load_page(base_url)
        current_messages = scraper.get_messages()
        previously_messages = scraper.get_previous_messages()
        messages_after_filters = scraper.compare_messages(current_messages, previously_messages)
        for key in messages_after_filters:
            scraper.send_message(messages_after_filters[key])
        scraper.add_records_to_previous_messages(messages_after_filters)
        print(messages_after_filters)


if __name__ == '__main__':
    while True:
        
        # browsers = ['firefox', 'chrome', "undetected_chromedriver"]
        browsers = ['firefox']
        for browser in browsers:
            try:
                app = App(browser)
                app.run()
                break
            except selenium.common.WebDriverException as _ex:
                logger.warning(f"Exception: {_ex}")
                
        time.sleep(300)