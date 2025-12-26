import os
import threading
import time
from urllib.parse import urljoin

from selenium.webdriver.common.by import By

from tools import WebDriver, Source


class Spider:

    def __init__(self, driver_path: str, source_id: int, driver_option: list=None):
        # 驱动参数（后续多线程使用）
        self.driver_path = driver_path
        self.driver_option = driver_option
        # 加载驱动
        self.webdriver = WebDriver(driver_path, driver_option)
        # 加载配置
        self.source = Source(r'./source/source.json', source_id)
        # 其他配置
        self.cf_clearance = None
        self.cookie = None
        self.browser = None
        # 菜单
        self.menu()

    def menu(self):
        print("====================")
        print("欢迎进入系统")
        print(self.source.source_name)
        print(self.source.source_url)
        if self.source.source_comment: print(self.source.source_comment)
        if self.source.source_cloudflare:
            print(f'请前往 {self.source.source_url} 手动获取 cf_clearance ')
            self.cf_clearance = input('cf_clearance: ')
        elif self.source.source_cookie:
            print(f'请前往 {self.source.source_url} 手动获取 cookie ')
            self.cookie = input('cookie: ')
        # 初始化浏览器
        print('初始化浏览器')
        self.browser = self.webdriver.start_browser()
        print("====================")
        print('1.搜索')
        print('2.阅读')
        print('3.下载')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self.search()
            elif flag == '2':
                self.read()
            elif flag == '3':
                self.download()
            elif flag == '6':
                self.browser.quit()
                break
            else:
                print('无此功能')
                continue
        print('退出系统')

    def search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        if self.source.source_ruleSearch is None:
            print('该源无法进行搜索！')
            return 0
        key = input('请输入关键字(exit 退出): ')
        if key == 'exit':
            return 0
        self.browser.get(self.source.source_url)
        if self.source.source_cloudflare:
            self.browser.add_cookie({'name': 'cf_clearance', 'value': self.cf_clearance})
            self.browser.refresh()
        if self.source.source_cookie:
            cookie_list = []
            for each in self.cookie.split(';'):
                k, v = each.split('=')
                cookie_list.append({'name': k, 'value': v})
            for each in cookie_list:
                self.browser.add_cookie(each)
            self.browser.refresh()
        input_box = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleSearch.input_box)
        input_box.clear()
        input_box.send_keys(key)
        submit_button = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleSearch.submit_button)
        submit_button.click()
        while True:
            print('Wait for 3s')
            time.sleep(3)
            chap_text = []
            chap_link = []
            link = self.browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleSearch.result_url)
            for each in link:
                chap_text.append(each.text)
                chap_link.append(each.get_attribute('href'))
            print('====================')
            print("name | url")
            for each in range(len(chap_text)):
                print(f'{chap_text[each]} | {chap_link[each]}'.replace(self.source.source_url, ''))
            print('====================')
            if self.source.source_ruleSearch.result_PageNext == '':
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
                    next_button = self.browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleSearch.result_PageNext)
                    if len(next_button) != 0:
                        next_button[-1].click()
                    else:
                        print('最后一页，结束搜索')
                        print('====================')
                        break
                    continue

    def read(self):
        print("====================")
        print("2.阅读")
        print("====================")
        url = input('请输入链接(exit 退出): ')
        if url == 'exit':
            return 0
        if self.source.source_url in url:
            self.browser.get(url)
        else:
            self.browser.get(urljoin(self.source.source_url, url))
        if self.source.source_cloudflare:
            self.browser.add_cookie({'name': 'cf_clearance', 'value': self.cf_clearance})
            self.browser.refresh()
        if self.source.source_cookie:
            cookie_list = []
            for each in self.cookie.split(';'):
                k, v = each.split('=')
                cookie_list.append({'name': k, 'value': v})
            for each in cookie_list:
                self.browser.add_cookie(each)
            self.browser.refresh()
        print('Wait for 3s')
        time.sleep(3)
        novel_name = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleBookInfo.name).text
        novel_author = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleBookInfo.author).text
        print(novel_name)
        print(novel_author)
        print("====================")
        # 章节目录
        chapter_list = self.browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleToc.chapter_url)
        if len(chapter_list) == 0:
            print('章节列表为空，请检查源')
            return 0
        print('获取章节成功')
        print(f'章节: {len(chapter_list)}')
        chapter = input('请选择序号(q 退出，0 开始): ')
        if chapter == 'q':
            return 0
        try:
            chapter = int(chapter)
        except BaseException:  # noqa
            print('输入异常，归 0')
            chapter = 0
        if chapter < 0:
            chapter = 0
        chapter_link = chapter_list[chapter].get_attribute('href')
        if chapter_link == '':
            print('章节链接异常，请检查源')
            return 0
        if 'http' not in chapter_link:
            chapter_link = urljoin(self.source.source_url, chapter_link)
        # 跳转阅读
        self.browser.get(chapter_link)
        while True:
            print('Wait for 3s')
            time.sleep(3)
            chapter_name = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleContent.content_name).text
            p_list = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleContent.content).text.splitlines()
            content = []
            for each in p_list:
                data = each.strip()
                if each == '':
                    continue
                else:
                    content.append(data)
            chapter_content = content
            print("------------------------")
            print(chapter_name)
            count = 0
            for each in chapter_content:
                print(each)
                if count == 5:
                    print("------------------------")
                    continue_print = input('继续打印(q 退出): ')
                    if continue_print == 'q':
                        print('结束打印')
                        print("------------------------")
                        break
                    else:
                        # print('继续打印')
                        print("------------------------")
                        count = 0
                else:
                    count += 1
            print("========================")
            # 下一章
            next_chapter = input('前往下一页或章(q 退出): ')
            if next_chapter == 'q':
                print('结束阅读')
                print("========================")
                break
            else:
                try:
                    next_button = self.browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleContent.page_next)
                    # self.browser.execute_script("arguments[0].click();", next_button)
                    if len(next_button) == 1:
                        next_button[0].click()
                    else:
                        next_button[-1].click()
                except BaseException:  # noqa
                    next_button = self.browser.find_element(By.CSS_SELECTOR, self.source.source_ruleContent.chapter_next)
                    # self.browser.execute_script("arguments[0].click();", next_button)
                    if len(next_button) == 1:
                        next_button[0].click()
                    else:
                        next_button[-1].click()

    def download(self):
        print("====================")
        print("3.下载")
        print("====================")
        result_file = './result'
        if not os.path.exists(result_file):
            os.mkdir(result_file)
        url = input('请输入链接(exit 退出): ')
        if url == 'exit':
            return 0
        if 'http' not in url:
            self.browser.get(urljoin(self.source.source_url, url))
        else:
            self.browser.get(url)
        if self.source.source_cloudflare:
            self.browser.add_cookie({'name': 'cf_clearance', 'value': self.cf_clearance})
            self.browser.refresh()
        if self.source.source_cookie:
            cookie_list = []
            for each in self.cookie.split(';'):
                k, v = each.split('=')
                cookie_list.append({'name': k, 'value': v})
            for each in cookie_list:
                self.browser.add_cookie(each)
            self.browser.refresh()
        print('Wait for 3s')
        time.sleep(3)
        # 章节目录
        chapter_list = self.browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleToc.chapter_url)
        if len(chapter_list) == 0:
            print('章节列表为空，请检查源')
            return 0
        print('获取章节成功')
        print(f'章节: {len(chapter_list)}')
        start = int(input('开始页(0 开始)：'))
        end = int(input('结束页(章节数 结束)：'))
        thread_number = int(input('线程数：'))
        download_list = range(start, end)
        quotient, remainder = divmod(len(download_list), thread_number)
        threads = []
        target_start = start
        if remainder != 0:
            target_end = target_start + quotient + remainder - 1
        else:
            target_end = target_start + quotient - 1
        for each in range(thread_number):
            print(f'线程分配：{target_start} to {target_end}')
            t = threading.Thread(target=self.novel_get, args=(target_start, target_end, result_file, url))
            threads.append(t)
            target_start = target_end + 1
            target_end = target_start + quotient - 1
        for t in threads:
            t.daemon = True
            t.start()
        for t in threads:
            t.join()
        return 0

    def novel_get(self, start, end, result_file, url):
        new_webdriver = WebDriver(self.driver_path, self.driver_option)
        new_browser = new_webdriver.start_browser()
        if 'http' not in url:
            new_browser.get(urljoin(self.source.source_url, url))
        if self.source.source_cloudflare:
            self.browser.add_cookie({'name': 'cf_clearance', 'value': self.cf_clearance})
            self.browser.refresh()
        if self.source.source_cookie:
            cookie_list = []
            for each in self.cookie.split(';'):
                k, v = each.split('=')
                cookie_list.append({'name': k, 'value': v})
            for each in cookie_list:
                self.browser.add_cookie(each)
            self.browser.refresh()
        time.sleep(3)
        chapter_list = new_browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleToc.chapter_url)
        if len(chapter_list) == 0:
            raise ValueError('Chapter is null')
        new_browser.execute_script("arguments[0].click();", chapter_list[start])
        while True:
            if start > end:
                break
            chapter_name = new_browser.find_element(By.CSS_SELECTOR, self.source.source_ruleContent.content_name).text
            for each in ['\\', '/', ':', '*', '?', "\"", '<', '>', '|']:
                if each in chapter_name:
                    chapter_name = chapter_name.replace(each, '')
            with open(f'{result_file}/{start+1} @= {chapter_name}.txt', 'wb') as f:
                content = new_browser.find_element(By.CSS_SELECTOR, self.source.source_ruleContent.content).text
                content = content.splitlines()
                # content.insert(0, chapter_name)
                for string in content:
                    if string == '':
                        continue
                    f.write(string.strip().encode('UTF-8'))
                    f.write('\n'.encode('UTF-8'))
            try:
                next_button = new_browser.find_elements(By.CSS_SELECTOR, self.source.source_ruleContent.page_next)
                # new_browser.execute_script("arguments[0].click();", next_button)
                if len(next_button) == 1:
                    next_button[0].click()
                else:
                    next_button[-1].click()
            except BaseException:  # noqa
                next_button = new_browser.find_element(By.CSS_SELECTOR, self.source.source_ruleContent.chapter_next)
                # new_browser.execute_script("arguments[0].click();", next_button)
                if len(next_button) == 1:
                    next_button[0].click()
                else:
                    next_button[-1].click()
            start += 1
            time.sleep(3)
        print('线程关闭')

if __name__ == '__main__':
    Spider(r'F:\Sdk\webdriver\geckodriver.exe', 1)
