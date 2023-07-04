# novel-spider

## 这是什么？

这个一个用来爬取网络小说的 Python 脚本。

为什么要编写这个？主要是希望能在 PyCharm 中阅读小说，在日常工作之余，放松心情（~~摸鱼~~）。


## 设计思路

脚本支持 Selenium 和 API 两种方式进行爬取，依据编写的书源，脚本自动选择对应方式对网站内容进行获取。

在使用 Selenium 爬取时，脚本将使用无头浏览器进行爬取，以模拟真实用户操作。（开发完毕）

- 模拟用户使用搜索框进行搜索。
- 通过链接前往书籍目录页，在书籍目录页选择章节点击。
- 在正文阅读中，模拟用户点击下一页来跳转下一章。

在使用 API 爬取时，脚本将使用 Requests 和 BeautifulSoup 进行爬取。（待开发）

## 难点

- 书源的适配，不同网站的界面样式不一致，如何确保脚本能通过统一的书源格式进行爬取。（这里统一使用 CSS Selector 对网站内容进行识别并爬取）
- Cloudflare 的人机验证绕过，部分网站使用 Cloudflare 的墙来避免爬虫爬取。（这里通过手动在安全的浏览器中获取 Cookie 值 `cf_clearance` 后再进行绕过）

## 书源

书源的编写参考了 [XIU2 / Yuedu](https://github.com/XIU2/Yuedu) 这个项目的 [书源文件](https://github.com/XIU2/Yuedu/blob/master/shuyuan) 。

需要注意的是，本项目的书源与 Yuedu 项目的书源并不通用，本项目的书源包含的信息更少（主要是麻烦）。

如果要将 Yuedu 的书源应用到本项目，则必须对书源的内容进行修改。用户需要从 Yuedu 的书源文件中查找对应页面的 CSS 选择器规则填入 `source/source.json` 这个文件夹内。

本项目的书源格式如下：

```json5
[
  {
    "bookSourceId": 1,  // 书源 ID，在 main.py 文件中切换来变更书源
    "bookSourceName": "书趣阁",  // 网站名称
    "bookSourceGroup": "selenium",  // 爬取方式
    "bookSourceComment": "",  // 注释，当注释中存在“异常”这两个字时，程序会中止，需要变更书源
    "bookSourceUrl": "https://www.ishuquge.org",  // 网络地址
    "cloudflare": false,  // 是否存在 cloudflare 防护
    "ruleSearch": {  // 搜索栏规则
      "inputBox": ".search .text",  // 搜索输入框规则
      "submitButton": ".search .btn",  // 搜索提交按钮规则
      "resultUrl": ".bookinfo a:nth-child(1)",  // 结果链接，链接必须为标签<a>，程序取 href 和 text 值为数据
      "resultPageNext": ""  // 下一页按钮规则
    },
    "ruleBookInfo": {  // 书籍信息
      "name": ".info h2",  // 书籍名称
      "author": ".small span:nth-child(1)"  // 书籍作者
    },
    "ruleToc": {  // 书籍目录
      "trueToc": "",  // 真实的书籍目录跳转按钮
      "chapterUrl": "dt:nth-of-type(2) ~ dd a"  // 章节链接，链接必须为标签<a>，程序取 href 和 text 值为数据
    },
    "ruleContent": {  // 正文
      "content": "#content",  // 正文，直接取整个正文框即可，不用取到<p>标签
      "contentName": ".content h1",  // 正文标题
      "pageNext": ".page_chapter li:nth-of-type(3) a"  // 下一页按钮
    }
  }
]
```