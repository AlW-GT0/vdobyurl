from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

from my16brow import get_rendered_content


def extract_mulist(html_content, condition='', condvalue=''):
    """ 从HTML内容中提取data-sl和titles
    Args: html_content (str): HTML字符串
    Returns: list: 包含字典的列表，每个字典有'sl_url'和'title'两个键
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # 查找所有的item元素
    items = soup.find_all('div', class_='item rank-a')
    
    result = []
    for item in items:
        # 提取data-sl属性
        data_sl = item.get('data-sl', '')
        # 提取titles内容
        title_div = item.find('div', class_='titles')
        title = title_div.get_text(strip=True) if title_div else ''
        # 只添加有有效数据的项
        if data_sl and title:
            if condition != '':
                # 筛选符合condition的数据项
                data_value = item.find('div', class_=condition).get_text(strip=True) if title_div else ''
                if data_value != condvalue:
                    continue
                # print(f'{data_value}')
            result.append(f'{title}::{data_sl}\n')
    result = list(set(result))
    return result

def getVdolist_1(domain, urlpath, output_dir):
    try:
        os.makedirs(output_dir)
    except:
        print('文件已存在')
    mupath = f'{output_dir}/mulist.txt'
    htmlpath = f'{output_dir}/0.html' # 将html文件保存的下载路径
    url = urljoin(domain, urlpath)

    get_rendered_content(url, htmlpath)
    file = open(htmlpath)
    # extract_video_data(现名extract_mulist)直接获取m3u8
    urls_mulist = extract_mulist(file.read())
    file.close()
    
    with open(mupath, "w") as f:
        f.write("")
    for murl in urls_mulist:
        with open(mupath, "a+") as f:
            f.write(murl)
            f.write(murl)

from datetime import datetime

def getVdolist_4novel(domain, output_dir):
    # 选择时间最新的，条件自然是'time'
    condition = 'time'
    today = datetime.now().strftime('%Y-%m-%d')
    # today = '2026-05-12'
    # print(today)
    output_dir = f'{output_dir}/{today}/'
    try:
        os.makedirs(output_dir)
    except:
        print('文件已存在')
    mupath = f'{output_dir}/mulist.txt'
    htmlpath = f'{output_dir}/0.html' # 将html文件保存的路径
    url = domain


    get_rendered_content(url, htmlpath)
    file = open(htmlpath)
    # 使用extract_video_data(现名extract_mulist)直接获取m3u8
    urls_mulist = extract_mulist(file.read(), condition, today)
    file.close()
    
    with open(mupath, "w") as f:
        f.write("")
    for murl in urls_mulist:
        with open(mupath, "a+") as f:
            f.write(murl)
            f.write(murl)
    # 返回文件路径
    return output_dir

# if __name__ == "__main__":
    # domain = 
    # urlpath =
    # output_dir =
    # getVdolist_1(domain, urlpath, output_dir)