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
        # todo add send to endpoint
        scraper = Scraper(self.browser, headless=False)
        scraper.load_page(base_url)
        current_messages = scraper.get_messages()
        previously_messages = scraper.get_previous_messages()
        messages_after_filters = scraper.compare_messages(current_messages, previously_messages)
        for message in messages_after_filters:
            scraper.send_message(message)
        # todo add messages and delete after 1000 records
        print(messages)


if __name__ == '__main__':
    while True:
        time.sleep(300)
        # browsers = ['firefox', 'chrome', "undetected_chromedriver"]
        browsers = ['firefox']
        for browser in browsers:
            try:
                app = App(browser)
                app.run()
                break
            except selenium.common.WebDriverException as _ex:
                logger.warning(f"Exception: {_ex}")