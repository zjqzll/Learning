#coding:utf8

# 导入需要使用的模块
import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException   # 捕捉异常(连接超时，读取超时，未知的服务器，代理连接不上，连接代理超时，代理读取超时，网络环境异常....)

# 尝试连接获取页面
def get_one_page(url):
    '''  获取网页 html 内容并返回   '''
    try:      # try(可能发生错误的语句放在 try)  except(处理异常)  else(当没有发生异常时，else中的语句将会被执行)  防止程序因为异常而中断。
        # 获取网页 html 内容
        response = requests.get(url)
        # 通过状态码来判断是否获取成功
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 正则匹配需要的内容
def parse_one_page(html):
    ''' 解析 HTML 代码，提取有用信息并返回  '''
    # 正则表达式进行解析
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?src=.*?data-src="(.*?)".*?name">'\
                         + '<a.*?>(.*?)</a>.*?"star">(.*?)</p>.*?releasetime">(.*?)</p>' \
                        + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    # data-src="(.*?)" 后加 > 和没有加 区别？
    # re.S 即为. 并且包括换行符在内的任意字符（.不包括换行符）
    # 匹配所有符合条件的内容
    # 用迭代进行异步操作
    items = re.findall(pattern, html)  # re.findall 返回的是一个list
    for item in items:
        yield{    # yield 生成器 generator， 可用于迭代（return返回一个值，并记住这个返回的位置，下次迭代就从这个位置后开始）
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

# 存储到文件中
def write_to_file(content):
    with open('E:/0 test/result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')  # 利用json.dumps 将字典转换成字符串的形式
        f.close()

# 配置启动函数
def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


# 使用多进程加速一秒完成（多线程：实现对多个 url 同时操作）
if __name__ == '__main__':
    pool=Pool()  # 创建进程池（将数组中的每个元素提取出来当做函数的参数，创建一个进程，放进进程池里）
    pool.map(main,[i*10 for i in range(10)])