#https://sites.google.com/a/chromium.org/chromedriver/downloads
#https://chromedriver.chromium.org/downloads
#http://chromedriver.storage.googleapis.com/index.html
#这是谷歌驱动的下载地址。
#############################################################
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 设置代理服务器和代理端口号
server = Server('/path/to/browsermob-proxy/bin/browsermob-proxy')
server.start()
proxy = server.create_proxy()

# 配置 Chrome Options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
# 加载谷歌浏览器驱动程序
driver = webdriver.Chrome(executable_path='C:\\Users\google_chrome\chromedriver', options=chrome_options)#这里填写谷歌驱动
# 开启网络捕获
proxy.new_har("google")
# 打开网站并等待页面加载完成
driver.get('http://www.gmail.com')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 等待元素加载完成，最多等待10秒
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "myElement"))
)
# 获取 HAR 文件内容并保存到本地文件中
har = proxy.har
with open('gmail.har', 'w') as f:
    f.write(json.dumps(har))
# 关闭浏览器和代理服务器
driver.quit()
server.stop()
