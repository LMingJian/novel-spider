import json


class Source:

    def __init__(self, json_path: str, source_id: int):
        with open(json_path, 'r', encoding='UTF-8') as json_file:
            json_data = json.load(json_file)
            source_id -= 1
            if source_id < 0 or source_id >= len(json_data):
                raise ValueError('source_id 的值非法')
            json_data = json_data[source_id]
        # 加载数据
        self.source_id = json_data['bookSourceId']
        self.source_name = json_data['bookSourceName']
        self.source_group = json_data['bookSourceGroup']
        self.source_comment = json_data['bookSourceComment']
        self.source_url = json_data['bookSourceUrl']
        self.source_cloudflare = json_data['cloudflare']
        self.source_cookie = json_data['cookie']
        # 加载复杂数据
        self.source_ruleSearch = RuleSearch(json_data['ruleSearch']) if json_data['ruleSearch']['enable'] else None
        self.source_ruleBookInfo = RuleBookInfo(json_data['ruleBookInfo'])
        self.source_ruleToc = RuleToc(json_data['ruleToc'])
        self.source_ruleContent = RuleContent(json_data['ruleContent'])



class RuleSearch:

    def __init__(self, data: dict):
        self.new_page = data['newPage']
        self.input_box = data['inputBox']
        self.submit_button = data['submitButton']
        self.result_url = data['resultUrl']
        self.result_PageNext = data['resultPageNext']


class RuleBookInfo:

    def __init__(self, data: dict):
        self.name = data['name']
        self.author = data['author']


class RuleToc:

    def __init__(self, data: dict):
        self.chapter_url = data['chapterUrl']


class RuleContent:

    def __init__(self, data: dict):
        self.content = data['content']
        self.content_name = data['contentName']
        self.page_next = data['pageNext']
        self.chapter_next = data['chapterNext']

if __name__ == '__main__':
    s = Source('../source/source.json', 1)
    print(s.source_name)
