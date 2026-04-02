import requests
from bs4 import BeautifulSoup
import gzip
from io import BytesIO

# 模拟Chrome浏览器的请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
# }
headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'utf-8, gzip, deflate',
        'Connection': 'keep-alive',
        'Sec-Ch-Ua-Platform': 'Android',
        'Cache-Control': 'max-age=0',
        'X-Requested-With': 'com.android.chrome'  # 关键标识
    }

domain = 'https://38d5.ty010bb.pro:6598/'
file = '/videoplay/?vid=94628'
url = domain+file
print(url)

try:
    # 发送HTTPS GET请求
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()  # 检查请求是否成功
        
    response.encoding = response.apparent_encoding
    # 获取HTML内容
    html_content = response.text
    
    # 打印响应状态码和头部
    print(f"状态码: {response.status_code}")
    # print(f"编码格式: {response.encoding}")
    print("\n响应头部:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    
    # 使用BeautifulSoup解析HTML并打印头部部分
    soup = BeautifulSoup(html_content, 'html.parser')
    print("\nHTML文件头部内容:")
    print(soup.head.prettify() if soup.head else "未找到<head>标签")
    
    # 将soup内容写入文件
    output_path = './html/content1.html'
    with open(output_path, 'w', encoding=response.encoding) as f:
        f.write(soup.prettify())  # 或者使用 soup.prettify() 使HTML格式更美观

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
except Exception as e:
    print(f"发生其他错误: {e}")