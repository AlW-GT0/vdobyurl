# from dloadVdo import dloadM3u8
from getUrls import getUrls, getUrls_1
# from getm3u8 import getHtml, extract_m3u8s

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def getam3u8list_1(domain, urlpath, output_dir):
    mupath = f'{output_dir}/mulist.txt'
    htmlpath = f'{output_dir}/0.html' # 将html文件保存的下载路径
    url = urljoin(domain, urlpath)
    with open(mupath, "w") as f:
        f.write("")
    murls = getUrls_1(url, htmlpath)
    for murl in murls:
        with open(mupath, "a+") as f:
            f.write(murl)
            f.write(murl)

def getVdolist_1(domain, urlpath, output_dir):
    try:
        os.makedirs(output_dir)
    except:
        print('文件已存在')
    mupath = f'{output_dir}/mulist.txt'
    getam3u8list_1(domain, urlpath, output_dir)

# if __name__ == "__main__":
    # domain = 
    # urlpath =
    # output_dir =
    # getVdolist_1(domain, urlpath, output_dir)