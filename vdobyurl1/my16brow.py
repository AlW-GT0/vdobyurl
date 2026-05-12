from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

from bs4 import BeautifulSoup
import time
import os

def setup_chromium_driver():
    chrome_options = Options()
    # 关键修复配置
    chrome_options.add_argument("--no-sandbox")  # 必须添加
    chrome_options.add_argument("--disable-dev-shm-usage")  # 必须添加
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--headless=new")  # 使用新版headless模式
    # 针对Snap安装的特殊配置
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--disable-setuid-sandbox")
    # 设置用户代理
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    chrome_options.add_argument(f"--user-agent={user_agent}")
    # 明确指定Chromium路径
    chrome_options.binary_location = "/snap/bin/chromium"
    # 尝试不同的ChromeDriver路径
    chromedriver_paths = [
        "/snap/chromium/current/usr/lib/chromium-browser/chromedriver",  # Snap专用路径
        # "/usr/bin/chromedriver", "/usr/lib/chromium-browser/chromedriver",
    ]
    # 移动设备模拟设置
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": user_agent
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    for path in chromedriver_paths:
        if os.path.exists(path):
            service = Service(
                executable_path=path,
                timeout=300,
            )
            try:
                driver = webdriver.Chrome(service=service, options=chrome_options)
                # 应用针对 iPhone 的 stealth 配置
                stealth(
                    driver,
                    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                    languages=["zh-CN", "zh", "en-US", "en"],
                    vendor="Apple Computer, Inc.",  # iPhone 的供应商是 Apple
                    platform="iPhone",  # iPhone 平台
                    webgl_vendor="Apple Inc.",  # iPhone 使用 Apple 的 WebGL
                    renderer="Apple GPU",  # iPhone 的 GPU 渲染器
                    fix_hairline=True,
                    run_on_insecure_origins=False,
                )
                print(f"成功使用ChromeDriver: {path}")
                return driver
            except Exception as e:
                print(f"路径 {path} 失败: {str(e)}")
                continue
    # 所有路径都失败时尝试自动查找
    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"自动查找也失败: {str(e)}")
        return None

def get_rendered_content(url, path=None, write=1):
    driver = setup_chromium_driver()
    if not driver:
        print("无法启动Chromium驱动")
        return None
    try:
        # 设置headers
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'X-Requested-With': 'com.apple.mobilesafari',
        }
        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})
        
        print(f"正在访问: {url}")
        driver.get(url)
        # 更智能的等待方式
        time.sleep(2)  # 基础等待
        max_wait = 30
        waited = 0
        while waited < max_wait:
            if driver.execute_script("return document.readyState") == "complete":
                break
            time.sleep(1)
            waited += 1
        
        rendered_html = driver.page_source
        soup = BeautifulSoup(rendered_html, 'html5lib')
        formatted_html = soup.prettify(formatter="html", encoding=None)
        if write == 1 and path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(formatted_html)
            print(f"内容已保存到: {path}")
        return formatted_html  
    except Exception as e:
        print(f"访问页面时出错: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # 使用示例
    url = "https://km.yvp1.pro:8869/"
    rendered_html = get_rendered_content(url, "./html/rendered_page.html")
    if rendered_html:
        soup = BeautifulSoup(rendered_html, 'html.parser')
        print("页面解析成功!")

    # # 现在可以解析渲染后的内容
    # result_div = soup.find('div', id='result')
    # page_div = soup.find('div', id='page')
