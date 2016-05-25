import urllib.request
import re
import http.cookiejar
import gzip
import pymysql

def gethtml(url):
    header = {
        'Connection': 'Keep-Alive',
        'Accept-Encoding':	'gzip, deflate, br',
        'Referer':	'https://www.zhihu.com/',
        'Cookie':	'q_c1=0a43f6e6126f4446b8a97aa401190685|1464053665000|1464053665000; cap_id="NTAxNTJmYjM4NTAyNDZhOGE3YmFjYjQ0OTE3MjAyYWY=|1464053665|b7654b3316d9b4f6dde6060d87681851bb86ea8a"; l_cap_id="Mzk0YTBlNWE4M2E1NDFiZWIzNjg2YjFiMWMxYjBiMWI=|1464053665|06dd95637060ecbbdbfcc9b96096e1f7e4e37b3f"; d_c0="AFBArjEt-AmPToKHlOcg8YKmgxFHwDvdoPI=|1464053668"; __utma=51854390.2103925672.1464053668.1464053668.1464137636.2; __utmz=51854390.1464053668.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20130320=1^3=entry_date=20130320=1; _za=b1f10beb-f107-4204-935e-591585e4f601; _zap=cd9ffad7-b266-4092-b875-45c66f01f4d2; login="NDcxZmM0NmQ1MzY5NGIxZWJmMzNhMjcwYTg4YzdiNGI=|1464053747|dae48986408753c85736823393e9394de5aea21a"; z_c0=Mi4wQUFBQTZvY2FBQUFBVUVDdU1TMzRDUmNBQUFCaEFsVk5EejFyVndDV2xOZFlNR3hlVUNMSmN6alZUTGp3bWlJd2xR|1464053775|556e89a042e7f2e97be1395ceef5b0a04faa6574; _xsrf=9de153f00d174d5fd6e7e149de988fba; __utmb=51854390.2.10.1464137636; __utmc=51854390; __utmt=1',
        'Host':	'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':	'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    result = []
    for key, value in header.items():
        elem = (key, value)
        result.append(elem)
    opener.addheaders = result
    op = opener.open(url)
    data = op.read()
    data = ungzip(data)
    return data


def ungzip(data):
    try:
        print('正在解压')
        data = gzip.decompress(data)
        print('解压完毕')
    except:
        print('为经压缩，无需解压')
    return data

'''
获得用户个人关注者列表页中的用户a标签
'''
def getfollowees(html):
    cer = re.compile(r'(?<=href="https://www.zhihu.com/people/).*?(?=" class=")')
    strlist = cer.findall(html)
    users = []
    for x in strlist:
        users.append(x)
    return users


'''
主函数
'''
followees_url = 'https://www.zhihu.com/people/jiao-niu-pai/followees'
html = gethtml(followees_url)
repl = html.decode().replace('\n', ' ')
#print(repl)
lists = getfollowees(repl)

file = open('users', 'a')
for x in lists:
    followees_url =  'https://www.zhihu.com/people/'+ x + '/followees'
    html = gethtml(followees_url)
    repl = html.decode().replace('\n', ' ')
    a = getfollowees(repl)
    for res in a:
        file.write(res + '\n')
file.close()
print("<br>ok")