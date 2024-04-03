import requests

url = 'https://www.hkexnews.hk/ncms/script/eds/activestock_sehk_c.json'

your_cookie = 'replace your cookie here'
your_user_agent = 'replace your user agent here'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': f'{your_cookie}',
    'Dnt': '1',
    'If-Modified-Since': 'Mon, 29 May 2023 08:57:40 GMT',
    'Referer': 'https://www.hkexnews.hk/index_c.htm',
    'Sec-Ch-Ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': f'{your_user_agent}'
}

response = requests.get(url, headers=headers)
res_js = response.json()

with open('stock_list.csv', 'a') as f:
    f.write('stock_id,stock_name,stock_code\n')
    for i in res_js:
        id = i['i'] # stockId
        name = i['n'] # stock name
        code = i['c'] # stock code
        f.write('{},{},{}\n'.format(id, name, code))
