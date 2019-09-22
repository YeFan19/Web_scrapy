from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = "https://www.dxueshi.com/task/index.php?c1=2&c2=0&c3=0&c4=0&c5=0&t1=0&a=0&o=0&st=0&t=0&kw=&page={}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}
page_num = 5
info = {}

def require_txt(requirements):
    require_txt = ''
    for i in requirements:
        require_txt = require_txt + str(i)
    require_txt = re.sub('<[\s\S]* ?>', ' ', require_txt).strip()
    return require_txt



result = pd.DataFrame(info)
for i in range(1, page_num):
    homepage_url = url.format(i)  # 分别将主页面取出
    rq = requests.get(homepage_url, headers)  # 生成请求
    soup = BeautifulSoup(rq.content, 'html.parser')  # 生成beautifulsoup对象
    subpages = re.findall('https://www.dxueshi.com/task/show[0-9]*?\.html', soup.prettify())  # 将beautifulsoup对象格式化，正则匹配子网页
    print('No{} is scrapying!'.format(i))
    title_li = []
    money_li = []
    requirement_li = []
    link_li = []
    # 对子网页进行操作
    for subpage in subpages:
        subrq = requests.get(subpage, headers)
        subsoup = BeautifulSoup(subrq.content, 'html.parser')
        title = subsoup.find(name='h1', attrs={'class': "flh1"}).string.strip()
        money = subsoup.find(name='h1', attrs={'class': "frh1"}).string.strip()
        requirements = subsoup.find(name='p', attrs=("content")).contents
        requirement = require_txt(requirements)
        title_li.append(title)
        money_li.append(money)
        requirement_li.append(requirement)
        link_li.append(subpage)

    info['Title'] = title_li
    info['Money'] = money_li
    info['Requirement'] = requirement_li
    info['Link'] = link_li
    df = pd.DataFrame(info)
    print(df)


    writer = pd.ExcelWriter('f://yf//PycharmProject//web_scrapy//data_result{}.xls'.format(i))
    df.to_excel(writer)
    writer.save()





