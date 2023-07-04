from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service


class WebDriver:

    def __init__(self, driver_path: str, driver_options: list):
        if 'chromedriver' in driver_path:
            self._options = ChromeOptions()
            self._webdriver = Chrome
        elif 'msedgedriver' in driver_path:
            self._options = EdgeOptions()
            self._webdriver = Edge
        elif 'geckodriver' in driver_path:
            self._options = FirefoxOptions()
            self._webdriver = Firefox
        else:
            raise ValueError("The driver is not supported. Please replace the driver")
        if driver_options:
            for each in driver_options:
                self._options.add_argument(each)
        self._driver_path = driver_path

    def start_browser(self):
        browser = self._webdriver(service=Service(executable_path=self._driver_path), options=self._options)
        # browser.implicitly_wait(6)
        browser.maximize_window()
        return browser
