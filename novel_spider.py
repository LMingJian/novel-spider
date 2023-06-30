import time

from selenium.webdriver.common.by import By

from tools import WebDriver, Source


class Spider:

    def __init__(self, driver_path: str, driver_option: list, source_id: int):
        webdriver = WebDriver(driver_path, driver_option)
        self._source = Source(r'./source/source.json', source_id)
        self._browser = webdriver.start_browser()
        self._menu()

    def _menu(self):
        print("====================")
        print("欢迎进入系统")
        print(self._source.source_name)
        print(self._source.source_comment)
        print("====================")
        print('1.搜索')
        print('2.阅读')
        print('3.下载')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self._search()
            elif flag == '2':
                self._read()
            elif flag == '3':
                self._download()
            elif flag == '6':
                self._browser.quit()
                break
            else:
                print('无此功能')
                continue
        print('退出系统')

    def _search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        key = input('请输入关键字(exit 退出): ')
        if key == 'exit':
            return 0
        self._browser.get(self._source.source_url)
        input_box = self._browser.find_element(By.CSS_SELECTOR, self._source.source_ruleSearch.input_box)
        input_box.clear()
        input_box.send_keys(key)
        submit_button = self._browser.find_element(By.CSS_SELECTOR, self._source.source_ruleSearch.submit_button)
        submit_button.click()
        while True:
            print('Wait for 6s')
            time.sleep(6)
            chap_text = []
            chap_link = []
            link = self._browser.find_elements(By.CSS_SELECTOR, self._source.source_ruleSearch.result_url)
            for each in link:
                chap_text.append(each.text)
                chap_link.append(each.get_attribute('href'))
            print('====================')
            print("name | url")
            for each in range(len(chap_text)):
                print(f'{chap_text[each]} | {chap_link[each]}'.replace(self._source.source_url, ''))
            print('====================')
            if self._source.source_ruleSearch.result_PageNext == '':
                print('结束搜索')
                print('====================')
                break
            else:
                print('存在下一页')
                next_page = input('前往下一页(q 退出): ')
                if next_page == 'q':
                    print('结束搜索')
                    print('====================')
                    break
                else:
                    next_button = self._browser.find_elements(By.CSS_SELECTOR,
                                                              self._source.source_ruleSearch.result_PageNext)
                    if len(next_button) != 0:
                        next_button[0].click()
                    else:
                        print('最后一页，结束搜索')
                        print('====================')
                        break
                    continue

    def _read(self):
        pass

    def _download(self):
        pass
