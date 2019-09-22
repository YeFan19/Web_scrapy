import requests  # 抓取网页
from bs4 import BeautifulSoup  # Python库，从HTML文件中提取数据，提供简单函数处理导航、搜索、修改分析树等功能
import re  # 正则：检索、替换符合某个模式的文本
import pandas as pd
import time

homepage = 'https://www.dxueshi.com/task/index.php?c1=2&c2=0&c3=0&c4=0&c5=0&t1=0&a=0&o=0&st=0&t=0&kw=&page{}'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}
PAGE_NUM = 10
SLEEP_TIME = 5
info = {}
df_columns = ['Title', 'Money', 'Requirement', 'Link']
for _ in df_columns:
    info[_] = []


def get_subpages(homepage_url):
    r = requests.get(homepage_url, headers=headers)  # 生成请求，requests.get(url, **kwargs)
    soup = BeautifulSoup(r.content, 'html.parser')  # 生成BeautifulSoup对象
    subpages = re.findall('href="(https://www.dxueshi.com/task/show[0-9]*?\.html)"', soup.prettify())
    #  soup.prettify()是格式化的BeautifulSoup对象
    #  re.findall(pattern, string, flags=0) pattern实例，表示转换后的正则表达式；string，表示输入的需要匹配的字符串；flags表示匹配模式。
    time.sleep(SLEEP_TIME)  # 程序等待SLEEP_TIME后退出

    return subpages


def get_content(subpage):
    r = requests.get(subpage, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find(name='h1', attrs={'class': "flh1"}).string.strip()  # str.strip()是将字符串str的头和尾的空格、\n \t之类删掉
    money = soup.find(name='h1', attrs={'class': 'frh1'}).string.strip()
    requirement = soup.find(name='p', attrs={'class': 'content'}).contents
    requirement_text = ''
    for _ in requirement:
        requirement_text = requirement_text + str(_)
    requirement_text = re.sub('<[\s\S]* ?>', ' ', requirement_text)  # sub(pat,repl,string[,count]=0) 将字符串中与模式pat匹配的子串都替换为repl
    requirement_text = requirement_text.replace('\n', '')
    time.sleep(SLEEP_TIME)  # .sleep(s),s拟休眠的时间，单位是秒，可以是浮点数

    return title, money, requirement_text


for homepage_num in range(1, PAGE_NUM+1):
    subpages = get_subpages(homepage.format(homepage_num))  # string.format(...)将字符串中用大括号分隔的字段替换为相应的参数，再返回结果
    print('No.{} homepage scrapied.'.format(homepage_num))
    for subpage in subpages:
        try:
            title, money, requirement = get_content(subpage)
            info['Title'].append(title)
            info['Money'].append(money)
            info['Requirement'].append(requirement)
            info['Link'].append(subpage)
            print('Page:{} scrapied'.format(subpage))
        except:
            print('Page:{} error!'.format(subpage))
            continue


    df = pd.DataFrame(info)
    df = df[df_columns]
    curr_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
    df.to_excel('F:\\yf\\PycharmProject\\Web_scrapy-master\\'+curr_time+'.xls')
