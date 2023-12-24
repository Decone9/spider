import requests

"""
巨潮网所有上市公司列表
"""

headers = {
    'Cookie': '',
    'Dnt': 1,
    'Host': 'www.cninfo.com.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = 'http://www.cninfo.com.cn/new/data/szse_stock.json'

json_data = requests.get(url, headers)
with open('stock_list.csv', encoding='utf-8', mode='a') as file:
    file.write('code,orgId,shortname\n')
    for i in json_data.json()['stockList']:
        file.write(f'{i["code"]},{i["orgId"]},{i["zwjc"]}\n')
