import pandas as pd
import requests
import time
from lxml import etree
from tqdm import tqdm
import io
import os

stock_df = pd.read_csv('stock_list.csv')

start_date = '20070625'
end_date = '20240403'

your_cookie = 'replace your cookie here'
your_user_agent = 'replace your user agent here'

url = 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Content-Length': '156',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': f'{your_cookie}',
    'Dnt': '1',
    'Origin': 'https://www1.hkexnews.hk',
    'Referer': 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh',
    'User-Agent': f'{your_user_agent}'
}

def download_pdf(url, filename, filepath):
    """
    :param url: 构建的PDF链接
    :param name: 文件名
    :return:
    """
    req = requests.get(url)  # 通过访问互联网得到文件内容
    bytes_io = io.BytesIO(req.content)  # 转换为字节流
    with open(f'./{filepath}/{filename}.pdf', 'wb') as file:
        file.write(bytes_io.getvalue())  # 保存到本地
    time.sleep(2)
    return bytes_io

while 1:
    name = input('请输入银行名称（繁体，输入1停止）：')
    if name == '1':
        break
    else:
        stockId = stock_df[stock_df['stock_name']==f'{name}']['stock_id'].values[0]
        payload = {
            'lang': 'ZH',
            'category': '0',
            'market': 'SEHK',
            'searchType': '1',
            'documentType': '-1',
            't1code': '40000',
            't2Gcode': '-2',
            't2code': '-2',
            'stockId': f'{stockId}',
            'from': f'{start_date}',
            'to': f'{end_date}',
            'MB-Daterange': '0',
        }

        response = requests.post(url, data=payload, headers=headers)
        html = response.text
        tree = etree.HTML(html)
        items = tree.xpath('//table[@role="grid"]/tbody/tr')

        pre_url = 'https://www1.hkexnews.hk' # a标签中的href属性提供的链接不全

        os.mkdir(f'./港股财报/{name}') # 构建PDF存储路径

        for item in tqdm(items): # 遍历所有的tbody中的tr标签
            bank_name = item.xpath('./td[3]/text()')
            title = item.xpath('./td[4]/div[@class="doc-link"]/a/text()')
            pdf_link = item.xpath('./td[4]/div[@class="doc-link"]/a/@href')
            file_name = bank_name[0].strip() + title[0].strip()
            url = pre_url + pdf_link[0] # 构建链接
            download_pdf(url, file_name, f'港股财报/{name}')
            time.sleep(4)