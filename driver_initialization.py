import time
from typing import Union, Literal
from fake_headers import Headers

# to add capabilities for chrome and firefox, import their Options with different aliases
from selenium.webdriver.chrome.options import Options as CustomChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as CustomFireFoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from seleniumwire import webdriver

try:
    import seleniumwire.undetected_chromedriver as uc
except Exception as _ex:
    print(_ex)

# import webdriver for downloading respective driver for the browser
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Initializer:
    def __init__(
            self,
            browser_name: Literal["chrome", "firefox", "undetected_chromedriver"],
            headless: bool,
            scale: Union[float, None] = None
    ):
        """Initialize Browser

        Args:
            browser_name (str): Browser Name
            headless (bool): Whether to run Browser in headless mode?
            scale (Union[float, None], optional): Optional parameter, if user wants to scale the interface (0.3 to 1).
                Defaults to None
      """
        self.browser_name = browser_name
        self.headless = headless
        self.scale = scale

    def set_properties(self, browser_option):
        """adds capabilities to the driver"""
        header = Headers().generate()['User-Agent']

        # Runs browser in headless mode
        if self.headless:
            browser_option.add_argument("--headless")

        browser_option.add_argument('--no-sandbox')
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument('--ignore-certificate-errors')
        browser_option.add_argument('--disable-gpu')
        browser_option.add_argument('--log-level=3')
        browser_option.add_argument('--disable-notifications')
        browser_option.add_argument('--disable-popup-blocking')
        browser_option.add_argument("--disable-blink-features=AutomationControlled")
        browser_option.add_argument("--disable-infobars")
        browser_option.add_argument("--disable-extensions")
        browser_option.add_argument('--user-agent={}'.format(header))

        if self.browser_name == 'firefox':
            browser_option.set_preference('intl.accept_languages', 'en-GB')
            browser_option.set_preference("dom.webdriver.enabled", False)
            browser_option.set_preference("useAutomationExtension", False)
        else:
            browser_option.add_argument("--lang=en-GB")

        if self.scale is not None:
            browser_option.add_argument(f"--force-device-scale-factor={self.scale}")
            browser_option.add_argument(f"--high-dpi-support={self.scale}")

        return browser_option

    def set_driver_for_browser(self, browser_name: str):
        """Expects browser name and returns a driver instance"""
        # if browser is supposed to be Chrome
        if browser_name.lower() == "chrome":
            browser_option = CustomChromeOptions()

            # Automatically installs chromedriver and initialize it and returns the instance
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.set_properties(browser_option)
            )

        # if browser is supposed to be `undetected_chromedriver`
        elif browser_name.lower() == "undetected_chromedriver":
            browser_option = uc.ChromeOptions()

            return uc.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.set_properties(browser_option)
            )

        # if browser is supposed to be Firefox
        elif browser_name.lower() == "firefox":
            browser_option = CustomFireFoxOptions()

            # Automatically installs geckodriver and initialize it and returns the instance
            try:
                return webdriver.Firefox(
                    service=FirefoxService(),
                    options=self.set_properties(browser_option)
                )
            except:
                return webdriver.Firefox(
                    service=FirefoxService(executable_path=GeckoDriverManager().install()),
                    options=self.set_properties(browser_option)
                )
        # if browser_name is not chrome either firefox than raise an exception
        else:
            raise Exception("Browser not supported!")

    def init(self):
        """Returns driver instance"""
        driver = self.set_driver_for_browser(self.browser_name)
        return driver


if __name__ == '__main__':
    driver = Initializer('firefox', False).init()
    driver.get('https://pypi.org/project/undetected-chromedriver/')
    time.sleep(50)