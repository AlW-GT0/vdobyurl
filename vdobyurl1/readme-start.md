### version 0.0
* 写下这段内容时，此版本已不适用"https://.pro:6788/"这一系列网站了

该网站另起炉灶，将内容转移到"https://.pro:8869/"网站上

采用了相对先进的脚本实时渲染，无法简单使用request获取信息

因此尝试vdobyurl1，通过chromium无头浏览器，实现更高级的信息获取

* 具体来讲，网站将mu链接存放在某一div的data-sl参数中，将对应的标题放在该链接div的上一层-div class="titles"-中

* vdobyurl1在my16brow.py中引入了

-- from selenium import webdriver

-- from selenium.webdriver.chrome.options import Options

-- from selenium.webdriver.chrome.service import Service
工具

### version 1.0
首先需要：
1、将原geturls中的方法替换为无头浏览器函数

* 开始写这段内容时，已实现v1.0(& v1.1)的无头浏览器获取方式，尚未开始v1.2版本

对于没将过程写进readme文件进行自我批评

### version 1.1
此版本主要工作是利用BeautifulSoup中的接口，优化数据获取逻辑

即将开展工作的版本
### version 1.2 


