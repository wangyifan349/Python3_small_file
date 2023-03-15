import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 获取谷歌浏览器User-Agent
def get_google_chrome_user_agent():
    ua = UserAgent()
    return ua.google

# 爬取图片并保存到本地
def save_image(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:# 以二进制写入的方式打开文件
        for chunk in response.iter_content(chunk_size=8192):#按块读取数据
            if chunk:#如果存在数据
                f.write(chunk)#写入数据
def save_hyperlinks(soup, links_file):#存储
    with open(links_file, 'a+') as f:
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                f.write(href + '\n')
# 爬取网页中的图片和文字
def crawl_images_and_text(url, img_folder, text_file):
    headers = {'User-Agent': get_google_chrome_user_agent()} # 使用谷歌浏览器User-Agent
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 保存图片
    images = soup.find_all('img')
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    for img in images:
        img_url = img.get('src')#获取图片的 URL 链接
        img_name = img_url.split('/')[-1]#提取图片名字
        save_path = os.path.join(img_folder, img_name)# 拼接保存路径
        save_image(img_url, save_path)# 保存图片到本地
    # 提取并保存文字
    with open(text_file, 'w') as f:
        for text in soup.stripped_strings:#遍历所有的字符串，并去除前后空格
            f.write(text + '\n')
    save_hyperlinks(soup, links_file)
    
if __name__ == '__main__':
    url = input("请输入要爬取的网址：")
    img_folder = input("请输入保存图片的文件夹：")
    text_file = input("请输入保存文字的文件名：")
    links_file = input("请输入保存超链接的文件名：")
    crawl_images_text_and_links(url, img_folder, text_file, links_file)
