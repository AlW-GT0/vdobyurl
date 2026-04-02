from bs4 import BeautifulSoup

from my16brow import get_rendered_content
# from getm3u8 import getHtml


url = "https://.pro:6598/category/?category_id=35&category_child_id=&page=2&limit=30"


def getUrls(url, path='./html/0.html', keyword='/videoplay/'):
    get_rendered_content(url, path) # getHtml(url, path)

    file = open(path)
    soup = BeautifulSoup(file.read(), 'html.parser')

    urlist = set()
    for tag in soup.find_all(['a', 'iframe', 'script', 'link'], href=True):
        urlist.add(tag['href'])
    for tag in soup.find_all(['img', 'video', 'audio', 'source'], src=True):
        urlist.add(tag['src'])
    
    print('查看urlist')
    print(urlist)
    print('查看完毕')
        
    videoplay_urls = [] # 4. 过滤包含 '/videoplay/' 的URL(x并转为绝对路径)
    for urli in urlist:
        if keyword in urli and url.startswith(('http://', 'https://')):
            videoplay_urls.append(urli)
            # absolute_url = urljoin(url, urli)  # 转换为绝对 URL
            # if absolute_url.startswith(('http://', 'https://')):
            #     videoplay_urls.append(absolute_url)
    return videoplay_urls


def extract_mulist(html_content):
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
        if data_sl and title:  # 只添加有有效数据的项
            result.append(f'{title}::{data_sl}\n')
    return result

# 采用 extract_video_data(现名extract_mulist)，直接获取m3u8
def getUrls_1(url, path='./html/0.html'):
    get_rendered_content(url, path) # getHtml(url, path)

    file = open(path)
    urls_mulist = extract_mulist(file.read())
    file.close()
    return urls_mulist

if __name__ == "__main__":
    path = './vdoutput/XP/tiaojiao/24'
    file = open(f'{path}/1.html')
    urls_mulist = extract_mulist(file.read())
    with open(f'{path}/mulist.txt', "w") as f:
        f.write('')
    with open(f'{path}/mulist.txt', "a+") as f:
        for murl in urls_mulist:
            f.write(murl)
            # f.write(murl)