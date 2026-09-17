from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json

from my16brow import get_rendered_content, find_m3u8, renew_url


def extract_data_href(soup, condition='', condvalue=''):
    """ 从 Soup 对象中提取 class 为 item rank-a 的容器中 data-href 值
    参数: soup: BeautifulSoup 对象
    返回: list: 包含所有匹配到的 data-href 值的列表
    """
    data_hrefs = []
    # 查找所有 class 为 "item rank-a" 的元素
    items = soup.find_all(class_="item rank-a")
    
    result = []
    for item in items:
        # 获取 data-href 属性值
        href = item.get("data-href")
        # 提取titles内容
        title_div = item.find('div', class_='titles')
        title = title_div.get_text(strip=True) if title_div else ''
        # 只添加有有效数据的项
        if href and title:
            if condition != '':
                # 筛选符合condition的数据项
                data_value = item.find('div', class_=condition).get_text(strip=True) if title_div else ''
                if data_value != condvalue:
                    continue
            # 否则不做筛选
            result.append(f'{title}::{href}')
    result = list(set(result))
    return result


def getVdolist2_1(domain, urlpath, output_dir):
    try:
        os.makedirs(output_dir)
    except:
        print('文件已存在')
    mupath = f'{output_dir}/mulist.txt'
    htmlpath = f'{output_dir}/0.html' # 将html文件保存的下载路径
    url = urljoin(domain, urlpath)

    html_content = get_rendered_content(url, write=0)
    soup = BeautifulSoup(html_content, 'html.parser')
    data_hrefs = extract_data_href(soup)
    # print(data_hrefs)

    mulist = []
    for data_href in data_hrefs:
        name, href = data_href.split("::")
        print(f"{name}, {href}")
        # url = urljoin(domain, href)
        
        murl = find_m3u8(domain, href)
        mulist.append(murl)
    return mulist


from datetime import datetime

def readconf(parameter = ''):
    filepath = f'./conf/{parameter}.conf'
    file = open(filepath, 'r')
    rst = file.readline()
    return rst.strip()
def renewconf(newdata, parameter = ''):
    filepath = f'./conf/{parameter}.conf'
    file = open(filepath, 'w')
    rst = file.write(newdata)
    return rst

def getVdolist2_4novel(output_dir):
    # 选择时间最新的，条件自然是'time'
    condition = 'time'
    today = datetime.now().strftime('%Y-%m-%d')
    # today = '2026-07-28'
    print(today)
    output_dir = f'{output_dir}/{today}/'
    try:
        os.makedirs(output_dir)
    except:
        print('文件已存在')
    mupath = f'{output_dir}/mulist.txt'
    htmlpath = f'{output_dir}/0.html' # 将html文件保存的下载路径
    domain = readconf('domain')
    print(f'初始域名为{domain}，开始获取新域名...')
    url = renew_url(domain, minute=60) # urljoin(domain, urlpath)
    rst = renewconf(url, 'domain')

    html_content = get_rendered_content(url, write=1)
    soup = BeautifulSoup(html_content, 'html.parser')
    data_hrefs = extract_data_href(soup, condition, today)
    print(data_hrefs)
    strlist = [
        '::'
    ] # 这一段原本调用的被注释了
    mulist = []
    for data_href in data_hrefs:
        name, href = data_href.split("::")
        print(f"{name}, {href}")
        # result = name
        # for substr in strlist:
        #     if substr in result:
        #         result = result.replace(substr, '[ban]')
        # name = result 这一段没有用，得重新考虑替换::的位置
        try:
            url = renew_url(url)
            murl = find_m3u8(url, href)
            if murl['sl'] == None:
                url = renew_url(url)
                murl = find_m3u8(url, href)
            print(f'得到murl：{murl}')
            murl['sl'] = f'{name}::{murl["sl"]}\n'
            murl['cdn'] = f'{name}::{murl["cdn"]}\n'
            mulist.append(murl)
        except Exception as e:
            print(f'遇到异常：\n{e}\n')
    
    with open(mupath, "w") as f:
        f.write("")
    for murl in mulist:
        with open(mupath, "a+") as f:
            f.write(murl['sl'])
            f.write(murl['cdn'])
    return output_dir # return mulist

def getVdolist_inhrefs(domain, dir):
    # read from dir/hrefs
    hrefs = f'{dir}/hrefs'
    mupath = f'{dir}/mulist.txt'
    hrefsfile = open(hrefs, 'r')
    url = renew_url(domain, minute=60)

    mulist = []
    while True:
        nameANDhref = hrefsfile.readline()
        if nameANDhref == '':
            break
        hrefsfile.readline()
        name, href = nameANDhref.split(',')
        print(f'{name},{href}')
        try:
            url = renew_url(url)
            murl = find_m3u8(url, href)
            if murl['sl'] == None:
                url = renew_url(url)
                murl = find_m3u8(url, href)
        except Exception as e:
            print(f'遇到异常：\n{e}\n')
        print(f'得到murl：{murl}')
        murl['sl'] = f'{name}::{murl["sl"]}\n'
        murl['cdn'] = f'{name}::{murl["cdn"]}\n'
        mulist.append(murl)

    with open(mupath, "w") as f:
        f.write("")
    for murl in mulist:
        with open(mupath, "a+") as f:
            f.write(murl['sl'])
            f.write(murl['cdn'])
    return output_dir # return mulist
    

if __name__ == "__main__":
    domain = "https://vo5x.ymp1.pro:8869/"
    urlpath = '' # "result.html?key=%E5%BC%A0"
    output_dir='./vdo4mnt/recent/260629/'
    
    import time
    start_time = time.time()
    mulist = getVdolist_inhrefs(domain, output_dir)
    end_time = time.time()
    print(f'dure {end_time - start_time}s')
    print(mulist)