try:
    from driver_utils import Utilities as SeleniumUtils
    from driver_initialization import Initializer, webdriver
except ModuleNotFoundError:
    from selenium_lib.driver_utils import Utilities as SeleniumUtils
    from selenium_lib.driver_initialization import Initializer, webdriver


__all__ = ['Initializer', 'SeleniumUtils', 'webdriver']