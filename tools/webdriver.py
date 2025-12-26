from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver.chrome.service import Service


class WebDriver:

    def __init__(self, driver_path: str, driver_options: list=None):
        if driver_options is None:
            driver_options = []
        if 'chromedriver' in driver_path:
            self._options = ChromeOptions()
            self._webdriver = Chrome
            self._service = Service(executable_path=driver_path)
            print('Current Driver Chrome')
        elif 'msedgedriver' in driver_path:
            self._options = EdgeOptions()
            self._webdriver = Edge
            self._service = Service(executable_path=driver_path)
            print('Current Driver Edge')
        elif 'geckodriver' in driver_path:
            self._options = FirefoxOptions()
            self._webdriver = Firefox
            self._service = FirefoxService(executable_path=driver_path)
            print('Current Driver Firefox')
        else:
            raise ValueError("The driver is not supported. Please replace the driver")
        # 加载配置
        if driver_options:[self._options.add_argument(each) for each in driver_options]

    def start_browser(self):
        browser = self._webdriver(service=self._service, options=self._options)
        # browser.implicitly_wait(2)
        browser.maximize_window()
        return browser

if __name__ == '__main__':
    driver = WebDriver(r'F:\Sdk\webdriver\geckodriver.exe')
    driver.start_browser()
