import requests
import time
import datetime
import logging
import sys
import json


from typing import Literal
from pathlib import Path

from selenium_lib import *
from selenium.webdriver.common.by import By

from fake_headers import Headers

logger = logging.getLogger()


class Scraper:

    driver: webdriver = None

    def __init__(
            self,
            browser_name: Literal['chrome', 'firefox', 'undetected_chromedriver'] = 'undetected_chromedriver',
            headless: bool = False,
            proxy: str | None = None
    ):
        # Save input parameters
        self.browser_name = browser_name
        self.headless = headless
        self.proxy = proxy

    def get_browser(self):
        """Init or get browser driver"""
        if self.driver is None:
            self.driver = Initializer(self.browser_name, self.headless, self.proxy).init()

            scale_factor = 0.5

            width = int(round(1450 / scale_factor))
            height = int(round(1200 / scale_factor))
            self.driver.set_window_size(width, height)

        return self.driver

    def load_page(self, url):
        def interceptor(request):
            # add the missing headers
            request.headers = Headers().generate()

        # Load page
        logger.info(f"Load page: {url}")
        self.get_browser()
        # self.driver.request_interceptor = interceptor
        self.driver.get(url)
        # SeleniumUtils.scroll_down(self.driver, 'down')
        # SeleniumUtils.wait_until_completion(self.driver)
        print('page was loading')

    @staticmethod
    def get_start_datetime():
        start_delta = datetime.timedelta(minutes=10)
        current_datetime = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=10)
        start_datetime = current_datetime - start_delta
        return start_datetime

    @staticmethod
    def find_trigger_word(message):
        # todo read trigger_word from file or from file 'constants'
        trigger_words = ['MVA', 'CAR FIRE', 'TRUCK FIRE']
        return set(message.lower().split()) & set([word.lower() for word in trigger_words])

    def get_messages(self):
        rows_css = 'tbody>tr'
        options_css = 'td'
        message_css = 'th'
        rows_data = self.driver.find_elements(By.CSS_SELECTOR, rows_css)
        messages = {}
        for row_data in rows_data:
            options_data = row_data.find_elements(By.TAG_NAME, options_css)
            datetime_text = options_data[0].text.strip()
            datetime_data = datetime.datetime.strptime(datetime_text, '%Y-%m-%d %H:%M')
            capcode_data = options_data[1].text.strip()
            agency_data = options_data[2].find_elements(By.TAG_NAME, 'span')[1].text.strip()
            # brigade_data = options_data[3].text
            message_data = row_data.find_element(By.TAG_NAME, message_css).text.strip()
            if datetime_data >= self.get_start_datetime() and agency_data.lower() == 'frnsw' and self.find_trigger_word(message_data):
                key = datetime_text + ' ' + capcode_data
                messages[key] = message_data
        return messages

    @staticmethod
    def send_message(message):
        url = f'http://103.230.157.122/~towsms/process_rfs.php'
        params = {
            'auth': '2349lkasdwedSDAA9jsd091823kjasdlkjasdlkjflksjadf3',
            'state': 'NSW',
            'message': message
        }
        # response = requests.post(url, params=params)
        # print(response.status_code)
        # print(response.text)
        print(message)

    @staticmethod
    def get_previous_messages():
        file_path = Path('../data/messages.json')
        if not file_path.exists():
            file_path.touch(exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('{}')
        with open(file_path, 'r', encoding='utf-8') as f:
            previous_messages = json.loads(f.read())
        return previous_messages

    @staticmethod
    def compare_messages(current_messages, previous_messages):
        for key in current_messages:
            if key in previous_messages and previous_messages[key] == current_messages[key]:
                del current_messages[key]
        return current_messages



        # todo messages contains MVA, CAR FIRE, TRUCK FIRE
        # todo list of trigger words

