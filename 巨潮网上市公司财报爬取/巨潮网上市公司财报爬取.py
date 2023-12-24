import requests
import pandas as pd
from urllib.parse import urlencode
import io
import time


def get_formdata(name):
    """
    :param name: 证券名称
    :return:
    """
    url = "http://www.cninfo.com.cn/new/information/topSearch/detailOfQuery"
    data = {
        'keyWord': name,
        'maxSecNum': 10,
        'maxListNum': 5,
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '70',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.cninfo.com.cn',
        'Origin': 'http://www.cninfo.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Pragma': 'no-cache',
        # 'Cookie': cookie, # cookie是与用户个人信息有关的内容，这里不需要
    }
    response = requests.post(url=url, headers=headers, data=urlencode(data))
    code = response.json()['keyBoardList'][0]['code']
    orgId = response.json()['keyBoardList'][0]['orgId']
    plate = response.json()['keyBoardList'][0]['plate']
    return code, orgId, plate


def download_pdf(url, name):
    """
    :param url: 构建的PDF链接
    :param name: 文件名
    :return:
    """
    response = requests.get(url)  # 通过访问互联网得到文件内容
    file = open(f'{name}.pdf', 'wb')
    file.write(response.content)  # 保存到本地


def get_pdf(code, orgId, plate, company, startDate, endDate):
    """
    :param code: get_formdata函数的返回值
    :param orgId: get_formdata函数的返回值
    :param plate: get_formdata函数的返回值
    :param company: 传入的公司名
    :param startDate: 开始爬取的日期
    :param endDate: 结束爬取的日期
    :return:
    """
    url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.cninfo.com.cn',
        'Origin': 'http://www.cninfo.com.cn',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    if plate == 'sse':
        column = 'sse'
        plate = 'sh'
    else:
        column = 'szse'
        plate = 'sz'
    data = {
        'stock': f'{code},{orgId}',
        'tabName': 'fulltext',
        'pageSize': 30,
        'pageNum': 1,
        'column': column,
        'category': 'category_ndbg_szsh;category_bndbg_szsh;',
        'plate': plate,
        'seDate': f'{startDate}~{endDate}',
        'searchkey': '',
        'secid': '',
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true',
    }

    response = requests.post(url=url, headers=headers, data=urlencode(data))
    reports_list = response.json()['announcements']
    for report in reports_list:  # 遍历所有财报
        if '摘要' in report['announcementTitle'] or 'H' in report['announcementTitle']:  # 筛掉摘要和H股报表
            continue
        else:
            pdf_url = "http://static.cninfo.com.cn/" + report['adjunctUrl']
            date = report['adjunctUrl'].split('/')[1]
            title = report['announcementTitle']
            file_name = f'{company}-{date}-{title}'
            try:
                download_pdf(pdf_url, file_name)
                print(f'{file_name}下载完成')
                time.sleep(2)
            except Exception as e:
                print(e)
                print(f'{file_name}下载失败')
                time.sleep(5)


if __name__ == '__main__':
    company_list = ['建设银行', '平安银行']  # 通过pandas读取csv/Excel文件传入
    # company_list = pd.read_excel()[''].tolist()
    # company_list = pd.read_csv()[''].tolist()
    start_date = '2021-05-01'
    end_date = '2023-12-19'
    for company in company_list:
        code, orgId, plate = get_formdata(company)
        get_pdf(code, orgId, plate, company, startDate=start_date, endDate=end_date)
