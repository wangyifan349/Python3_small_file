import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
def get_soup(url):
    """
    根据给定的URL获取BeautifulSoup对象
    :param url: 要请求的URL
    :return: BeautifulSoup对象或者None（如果请求出错）
    """
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")
        return None

def get_links(soup, base_url):
    """
    从BeautifulSoup对象中提取所有超链接
    :param soup: BeautifulSoup对象
    :param base_url: 当前页面的URL，用于将相对URL转换为绝对URL
    :return: 超链接列表
    """
    links = []
    for a in soup.find_all('a', href=True):
        link = urljoin(base_url, a['href'])
        links.append(link)
    return links

def clean_text(text):
    """
    清理文本，删除不必要的换行符和多余的空白字符
    :param text: 要清理的文本
    :return: 清理后的文本
    """
    return ' '.join(text.split())

def save_text(soup, title):
    """
    将提取到的文本内容保存到文件中，避免文件名重复
    :param soup: BeautifulSoup对象
    :param title: 网页标题
    """
    text = clean_text(soup.get_text())
    index = 1
    filename = title + '.txt'

    # 处理文件名重复的问题
    while os.path.exists(filename):
        filename = f"{title}_{index}.txt"
        index += 1

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"已保存：{filename}")

def crawl(url, depth):
    """
    爬取指定深度的链接并保存文本内容
    :param url: 要爬取的URL
    :param depth: 爬取深度
    """
    if depth == 0:
        return

    soup = get_soup(url)
    if soup:
        title = soup.title.string.strip()
        save_text(soup, title)

        links = get_links(soup, url)
        for link in links:
            crawl(link, depth - 1)

def main():
    start_url = input("请输入起始URL: ")
    max_depth = int(input("请输入爬取深度: "))

    crawl(start_url, max_depth)

if __name__ == "__main__":
    main()
