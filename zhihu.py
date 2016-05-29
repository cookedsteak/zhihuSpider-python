import spider
import re
from connection import Conn
from model import Users
from bs4 import BeautifulSoup

header = {
    'Connection': 'Keep-Alive',
    'Accept-Encoding':	'gzip, deflate, br',
    'Referer':	'https://www.zhihu.com/',
    #cookie here
    'Host':	'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':	'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}

url_followees = 'https://www.zhihu.com/people/jiao-niu-pai/followees'
url_followers = 'https://www.zhihu.com/people/jiao-niu-pai/followers'
url_info = 'https://www.zhihu.com/people/jiao-niu-pai'


def getpageinfo(username):
    '''
    获得用户主页的信息
    :param username:
    :return: userinfo array
    '''
    url_temp = 'https://www.zhihu.com/people/' + username
    spider_temp = spider.Spider(header=header, url=url_temp)
    subject = spider_temp.getHtml(type='raw')
    user = {}
    user['showname'] = re.search('(?<=<div class="title-section ellipsis"><span class="name">).*?(?=</span>)', subject).group()
    user['username'] = username
    user['followees'] = re.search('(?<=<span class="zg-gray-normal">关注了</span><br /><strong>).*?(?=</strong>)', subject).group()
    user['followers'] = re.search('(?<=<span class="zg-gray-normal">关注者</span><br /><strong>).*?(?=</strong>)', subject).group()
    return user

def getfollowees(data):
    '''
    获得用户关注着页的关注者
    :param data:
    :return: followees array
    '''
    cer = re.compile(r'(?<=href="https://www.zhihu.com/people/).*?(?=" class=")')
    str = cer.findall(data)
    return str


if __name__ == '__main__':
    # start db session
    conn = Conn().session
    # use cookie to get personal page and info
    spiderman = spider.Spider(header=header, url=url_followers)
    page = spiderman.getHtml(type='raw')
    # get followees
    followees = (getfollowees(page))
    # save followees-info (for in)


    for val in followees:
        userinfo = getpageinfo(val)
        print(userinfo)
        # print(getUsername(val))
        # print(getShowname(val))