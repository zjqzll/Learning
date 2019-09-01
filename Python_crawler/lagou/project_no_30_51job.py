# coding:utf-8
import requests
from requests.exceptions import RequestException
import time
import pandas as pd
import math
import json
import xlwt


def get_json(num):
    try:
        url_start = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=&labelWords=hot'
        url_parse = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'
        headers = {
            'Accept': 'application / json, text / javascript, * / *; q = 0.01',
            'Accept - Encoding': 'gzip, deflate, br',
            'Connection': 'keep - alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?px=default&city=%E5%85%A8%E5%9B%BD',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = {
            'first': 'true',
            'pn': num,
            'kd': '数据分析'
        }
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取 cookies
        cookie = s.cookies  # 为此次获取的 cookies
        response = requests.post(url_parse, headers=headers, data=data,
                                 cookies=cookie, timeout=3)  # 获取此次文本
        time.sleep(5)
        response.encoding = 'utf-8'
        # if response.content:
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        return None


def get_page_num(count):
    res = math.ceil(count / 15)
    # if res > 30:
    #     return 30
    # else:
    return res


# 获取 url 对应的源码
def parse_page_info(items):
    temps = []
    for item in items:
        temp = {
            'companyFullName': item['companyFullName'],
            'companyShortName': item['companyShortName'],
            'companySize': item['companySize'],
            'city': item['city'],
            'district': item['district'],
            'positionName': item['positionName'],
            'salary': item['salary'],
            'workYear': item['workYear'],
            'education': item['education'],
            'positionAdvantage': item['positionAdvantage']
        }
        temps.append(temp)
    return temps


def main():
    page1 = get_json(1)
    print(page1)
    total_count = page1['content']['positionResult']['totalCount']
    num = get_page_num(total_count)
    time.sleep(20)  # 推迟调用线程的运行,t表示推迟执行的秒数；
    print('职位总数：{},页数：{}'.format(total_count, num))
    n_info_total = []
    workbook = xlwt.Workbook(encoding='utf-8')
    Sheet1 = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
    columns = ['companyFullName', 'companyShortName', 'companySize',
               'city',
               'district', 'positionName', 'salary', 'workYear',
               'education',
               'positionAdvantage']

    for n in range(1, num + 1):
        # total_info = []
        html_info = get_json(n)
        job_list = html_info['content']['positionResult']['result']
        # print(type(job_list))
        if job_list == []:
            break
        else:
            page_info = parse_page_info(job_list)
            # total_info.append(page_info)
            print('已经爬取第{}页，职位总数：{}'.format(n, len(page_info)))
            time.sleep(30)
            info_total = []
            for i in range(len(page_info)):
                info = page_info[i].values()
                info = list(info)
                print(info)
                info_total.append(info)
            for t in range(len(columns)):
                # print(t)
                Sheet1.write(0, t, columns[t])
            for q in range(len(info_total)):
                for a in range(len(columns)):
                    Sheet1.write(q + 1 + (n - 1) * (len(page_info)), a,
                                 info_total[q][a])
                    # print(info_total[q][a])

    print(n)
    workbook.save(r'E:/0 test/51jobdata.xls')
    print('完成保存')


if __name__ == "__main__":
    main()
