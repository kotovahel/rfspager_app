import time
import logging

from typing import Literal

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from random import randint

logger = logging.getLogger(__name__)


class Utilities:
    """
    this class contains all the method related to driver behaviour,
    like scrolling, waiting for element to appear, it contains all static
    method, which accepts driver instance as a argument

    @staticmethod
    def method_name(parameters):
    """

    @staticmethod
    def wait_until_css_appear(driver, css_selector: str) -> None:
        """Wait for tweet to appear. Helpful to work with the system facing
        slow internet connection issues
        """
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'css_selector')))
        except WebDriverException:
            logger.exception(
                f"The item '{css_selector}' did not appear!, Try setting headless=False to see what is happening")

    @staticmethod
    def scroll_down(driver, scroll_type: Literal['random', 'screen', 'down']) -> None:
        """
            Helps to scroll down web page

            :param driver: webdriver  Selenium instance
            :param scroll_type: str Literal['random', 'screen', 'down']
                        screen      scroll by typing `pd_down` key
                        random      scroll down randomly (from 1 to 3 'screen')
                        down        scroll down to document Height (scroll till bottom)
        """
        try:
            if scroll_type == 'random':
                body = driver.find_element(By.CSS_SELECTOR, 'body')
                for _ in range(randint(1, 3)):
                    body.send_keys(Keys.PAGE_DOWN)

            elif scroll_type == 'screen':
                body = driver.find_element(By.CSS_SELECTOR, 'body')
                body.send_keys(Keys.PAGE_DOWN)

            elif scroll_type == 'down':
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        except Exception as ex:
            logger.exception("Error at scroll_down method {}".format(ex))

    @staticmethod
    def wait_until_completion(driver) -> None:
        """waits until the page have completed loading"""
        try:
            state = ""
            while state != "complete":
                time.sleep(randint(3, 5))
                state = driver.execute_script("return document.readyState")
        except Exception as ex:
            logger.exception('Error at wait_until_completion: {}'.format(ex))

    @staticmethod
    def delete_element(driver, css_selector):
        """
            Deletes the specified css selector from HTML

            :param driver: Webdriver
            :param css_selector: str  CSS selector to delete (with no double quotation marks)
        """

        delete_script = f'''
        var element = document.querySelector("{css_selector}");
        if (element)
            element.parentNode.removeChild(element);
        '''
        driver.execute_script(delete_script)
