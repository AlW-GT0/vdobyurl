### version 0.0
* 写下这段内容时，此版本已不适用"https://0f7c.ty015fv.pro:6788/"这一系列网站了

该网站另起炉灶，将内容转移到"https://vy5x.yur33kp1.pro:8869/"网站上

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

### version 1.2
该网站在旧网页的网址更新上出现了很大问题，具体来说，当前的图标会对应旧的链接，使得程序总是获取到错误的url，针对这一问题进行改进将是version 2的内容，我们将在version 1.2中实现获取当日新上传的视频

实现makenovel:
-通过添加筛选获取time为当天的容器
-增加html获取结果的去重
-发现单线程无法完成当日的任务，采用双线程

* 获取视频网页后获取url

260513
该网页构造形如https://mc.jl.com:15610/index.m3u8?sign=20f5a74402032469eb1102ce641155ff&t=1778608109的请求链接，为拿到sign与t，将在version 2中进一步改进无头浏览器，模拟完整执行流程获取资源

### version 2


