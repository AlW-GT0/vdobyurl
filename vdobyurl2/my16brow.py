from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium_stealth import stealth
from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
import re
from urllib.parse import urljoin

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

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def find_m3u8(domain, href):
    url = urljoin(domain, href)
    with sync_playwright() as p:
        iphone = p.devices["iPhone 14 Pro"]
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-features=NetworkService",
            ],
            executable_path="/snap/bin/chromium",
        )
        context = browser.new_context(
            **iphone,
            locale="zh-CN",
            extra_http_headers={
                "Referer": domain,
                "Origin": domain,
            },
        )
        page = context.new_page()
        page.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>false})"
        )

        m3u8_urls = {'sl': None, 'cdn': None}
        # ✅ 只拦截解析接口
        def on_response(res):
            if "/v2m/videoplay" in res.url:
                try:
                    data = res.json()
                    video = data.get("video", {})
                    sl = video.get("sl")
                    cdn = video.get("self_cdn_path")
                    if sl:
                        m3u8_urls['sl'] = sl
                    if cdn and cdn not in m3u8_urls:
                        m3u8_urls['cdn'] = cdn
                    print("✅ 解析接口返回 m3u8：")
                    print("SL:", sl)
                    print("CDN:", cdn)
                except Exception as e:
                    print("❌ 解析接口响应异常：", e)
            # else:
            #     print('空的m3u8list，但是抛出异常\n')
            #     raise PlaywrightTimeoutError
        page.on("response", on_response)

        # ✅ 不再监听 request / 不再等 m3u8
        try:
            page.goto(url, timeout=100000, wait_until="domcontentloaded")
        except PlaywrightTimeoutError as e:
            raise e # ✅ 明确只重抛 TimeoutError
        except Exception as e:
            print(e)
        # 触发解析
        page.mouse.wheel(0, 800)
        page.evaluate("""
            document.querySelectorAll('video').forEach(v => v.play());
        """)
        page.wait_for_timeout(20000)
        browser.close()
        if not m3u8_urls:
            print('空的m3u8list，但是抛出异常\n')
            raise PlaywrightTimeoutError
        return m3u8_urls

def get_final_url(start_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        final_url = start_url
        def on_navigate(frame):
            nonlocal final_url
            if frame == page.main_frame:  # 只记录主框架
                final_url = frame.url
        page.on("framenavigated", on_navigate)
        try:
            page.goto(start_url, timeout=60000, wait_until="domcontentloaded")
        except PlaywrightTimeoutError as e:
            return None # raise e # ✅ 明确只重抛 TimeoutError
        except Exception as e:
            print(e)
        browser.close()
        return final_url

def renew_url(start_url, target_ends=['.pro:8869/'], minute=5):
    current_minute = datetime.now().minute
    if minute <= 0:
        minute = 60
    # 检查是否处于每小时的前 minute 分钟
    if current_minute >= minute:
        # print(f"当前时间不在前5分钟内（当前第{current_minute}分钟），跳过监测")
        return start_url
    
    attempt_count = 0
    max_attempts = 30  # 最多尝试30次，防止无限循环
    while attempt_count < max_attempts:
        attempt_count += 1
        print(f"第{attempt_count}次尝试...")
        try:
            final_url = get_final_url(start_url)
            time.sleep(2)
            if final_url is None:
                print("  获取URL失败（超时或其他错误）")
                continue
            elif final_url == start_url:
                print("  获取到旧的URL")
                continue
            print(f"  当前最终URL: {final_url}")

            # 检查URL是否以目标后缀结尾
            for target_end in target_ends:
                if final_url.rstrip('/').endswith(target_end.rstrip('/')):
                    print(f"✅ 成功！找到目标URL: {final_url}")
                    return final_url
            print(f"  未匹配目标后缀，继续监测...")
        except Exception as e:
            print(f"  发生异常: {e}")
        # 间隔2秒再进行下一次检测
        time.sleep(2)
    print(f"❌ 超过最大尝试次数({max_attempts})，未找到目标URL")
    return start_url



if __name__ == "__main__":
    # 使用示例
    domain = "https://ru7t.yop1.pro:8869/"
    urlpath = "video.html?vid=135758"
    # rendered_html = get_rendered_content(url, "./html/rendered_page.html")
    # if rendered_html:
    #     soup = BeautifulSoup(rendered_html, 'html.parser')
    #     print("页面解析成功!")
    new_domain = renew_url(domain)
    print(new_domain)
    exit()
    m3u8_urls = find_m3u8(domain, urlpath)
    if m3u8_urls:
        print(f"\n最终获取到的完整m3u8链接:")
        print(m3u8_urls)


