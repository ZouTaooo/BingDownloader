import os
from time import sleep
import requests
from lxml import etree

headers = {
    'authority': 'cn.bing.com',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version': '"94.0.4606.54"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-model': '',
    'sec-ch-ua-platform': '"Windows"',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://cn.bing.com/images/search?q=%E6%8B%9C%E7%99%BB%20%E5%90%88%E5%BD%B1&qs=n&form=QBIR&sp=-1&pq=%E6%8B%9C%E7%99%BB%20%E5%90%88%E5%BD%B1&sc=5-5&cvid=0FDC897B0D1347DA8A1989CA95BAB160&first=1&tsc=ImageBasicHover',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'MMCA=ID=41FDCA62D4214FCFB38AFA784AD93140; _EDGE_V=1; MUID=1835E255FF8563DB0AD3F2EEFEAB62E2; SNRHOP=I=&TS=; MUIDB=1835E255FF8563DB0AD3F2EEFEAB62E2; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=E301236F01B24EFF95CBA263284C5480&dmnchg=1; _SS=SID=1B35FBF82CD76C332CDEEB432DF96D31; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMS0wOS0yM1QwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjJ9; ipv6=hit=1632368632395&t=4; _ITAB=STAB=TR; SRCHUSR=DOB=20210923&T=1632365032000&TPC=1632365037000; SUID=M; _EDGE_S=F=1&SID=1B35FBF82CD76C332CDEEB432DF96D31&ui=zh-cn; SRCHHPGUSR=SRCHLANG=zh-Hans&BRW=NOTP&BRH=M&CW=619&CH=912&SW=1920&SH=1080&DPR=1&UTC=480&DM=1&WTS=63767961832&HV=1632365384',
}


def request_download(PictureList, url, dir='upload_pic'):
    print("下载Bing图片: %s" % url)
    r = requests.get(url)
    sleep(0.5)
    filename = url.split("/")[-1]
    filename = filename.split("?")[0]

    PictureList.append(filename+'.jpg')
    with open('./' + dir + '/' + filename + '.jpg', 'wb') as f:
        f.write(r.content)


def download(path, query='', final=10):
    first = 0
    count = 35
    results = []

    result = os.path.exists(path)
    if not result:
        os.mkdir(path)

    while count <= 35:
        params = (
            ('q', query),
            ('first', str(first)),
            ('count', str(count)),
            ('cw', '1177'),
            ('ch', '912'),
            ('relp', '35'),
            ('tsc', 'ImageBasicHover'),
            ('datsrc', 'I'),
            ('layout', 'RowBased_Landscape'),
            ('mmasync', '1'),
            ('dgState', 'x*643_y*1362_h*180_c*2_i*36_r*8'),
            ('IG', '50728F4EDAA0464EAEA130852983A4D5'),
            ('SFX', '2'),
            ('iid', 'images.5534'),
        )

        try:
            response = requests.get(
                'https://cn.bing.com/images/async', headers=headers, params=params)
            # print(response.text)
            html = etree.HTML(response.text)
            # print(html)
            ret = html.xpath("//img[@class='mimg']/@src")
            results += ret
        except Exception as e:
            print("网络请求出错 %s" % str(e))

        first = count
        count += 35

    temp = set(results)
    PictureList = []
    count = 0
    for url in temp:
        try:
            request_download(PictureList=PictureList, url=url, dir=path)
        except Exception as e:
            print("图片下载出错 url: %s error: %s" % (url, str(e)))
        if count >= final:
            break


if __name__ == '__main__':
    print("start")
    download("./store_path", "关键字", 100)
