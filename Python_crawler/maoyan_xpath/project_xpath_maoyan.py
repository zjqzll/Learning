#coding:utf8
import requests
import re
from multiprocessing import Pool
from requests.exceptions import RequestException
from lxml import etree
import json

def get_one_page(url,headers):
    try:
        response = requests.get(url, headers = headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(content):
    html = etree.HTML(content)   # 解析提取 html 页面数据方式
    index = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/i/text()')
    image = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/a/img[2]/@data-src')
    title = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[1]/a/text()')
    actor = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[2]/text()')
    time = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[3]/text()')
    scores_1 = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[2]/p/i[1]/text()')
    scores_2 = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[2]/p/i[2]/text()')
    temps = []
    for i in range(len(index)):
        temp = {
            'index': index[i],
            'image': image[i],
            'title': title[i],
            'actor': actor[i].strip()[3:],
            'time': time[i].strip()[5:],
           'scores1': scores_1[i]+scores_2[i]           # 有电影无评分；索引超出范围
        }
        temps.append(temp)
    return temps

def write_to_file(temps):
    with open(r'E:/0 test/x_maoyan.txt','a',encoding = 'utf8') as f:
        f.write(json.dumps(temps, ensure_ascii = False)+'\n')
        f.close()

def main(offset):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    content = get_one_page(url,headers = headers)
    temp = parse_one_page(content)
    # for temp in parse_one_page(content):
    for t in range(len(temp)):
        print(temp[t])
        write_to_file(temp[t])

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[j*10 for j in range(10)])

