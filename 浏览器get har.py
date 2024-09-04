from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# 启动 BrowserMob Proxy 服务器
server = Server("/path/to/browsermob-proxy")  # 替换为 BrowserMob Proxy 的路径
server.start()
proxy = server.create_proxy()

# 配置 Selenium 使用代理
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy.proxy}")

# 配置 ChromeDriver 的路径
service = Service("/path/to/chromedriver")  # 替换为 ChromeDriver 的路径

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 开始捕获网络流量
    proxy.new_har("example", options={'captureContent': True})

    # 导航到目标网页
    driver.get("http://www.example.com")

    # 等待页面完全加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # 获取 HAR 数据
    har_data = proxy.har

    # 保存 HAR 数据到文件
    with open("output.har", "w") as har_file:
        json.dump(har_data, har_file, indent=4)

finally:
    # 关闭浏览器和 Proxy 服务器
    driver.quit()
    server.stop()
