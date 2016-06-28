import spider
import re
from connection import Conn
from model import Users
import queue
import threading

myCookie = 'Your Cookie Here'

myHeader = {
    'Connection': 'Keep-Alive',
    'Accept-Encoding':	'gzip, deflate, br',
    'Referer':	'https://www.zhihu.com/',
    'Cookie':	myCookie,
    'Host':	'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':	'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}


def getpageinfo(username, header):
    '''
    get personal page information
    :param username:
    :param header:
    :return: user array
    '''
    url_temp = 'https://www.zhihu.com/people/' + username
    spider_temp = spider.Spider(header=header, url=url_temp)
    subject = spider_temp.getHtml(type='raw')
    user = {}
    user['showname'] = re.search('(?<=<div class="title-section ellipsis"><span class="name">).*?(?=</span>)', subject).group()
    user['username'] = username
    user['followees'] = re.search('(?<=<span class="zg-gray-normal">关注了</span><br /><strong>).*?(?=</strong>)', subject).group()
    user['followers'] = re.search('(?<=<span class="zg-gray-normal">关注者</span><br /><strong>).*?(?=</strong>)', subject).group()
    try:
        user['focus'] = re.search('(?<=<span class="business item" title=").*?(?=">)', subject).group()
    except:
        user['focus'] = '未知'
    return user


def getuserlists(username, header, ftype='followers'):
    '''
    get User followers/followees Lists
    :param username:
    :param header:
    :param ftype: which list do you wanna get
    :return: str array
    '''
    url = 'https://www.zhihu.com/people/' + username + '/' + ftype
    spiderMan = spider.Spider(header=header, url=url)
    page = spiderMan.getHtml(type='raw')
    cer = re.compile(r'(?<=href="https://www.zhihu.com/people/).*?(?=" class=")')
    str = cer.findall(page)
    return str


def climbMain(conn, queue):
    fol = queue.get_nowait()
    # get followers strings
    followers = (getuserlists(username=fol.username, header=myHeader, ftype='followers'))

    for val in followers:
        # get followers info
        userInfo = getpageinfo(username=val, header=myHeader)
        print(userInfo['showname'])
        user = Users(
                username=userInfo['username'],
                showname=userInfo['showname'],
                followees=userInfo['followees'],
                followers=userInfo['followers'],
                focus=userInfo['focus'],
                fr_status=0,
                fe_status=0
                )
        conn.add(user)
        conn.commit()

    conn.query(Users).filter(Users.id == fol.id).\
        update({Users.fr_status:1}, synchronize_session=False)

    print('++++++'+fol.showname+'finished++++')


class MyClimberThread(threading.Thread):
    def __init__(self, threadno, connection, queue):
        threading.Thread.__init__(self, name=threadno)
        self.connection = connection
        self.queue = queue

    def run(self):
        climbMain(self.connection, self.queue)


if __name__ == '__main__':
    # start db session
    conn = Conn().session
    # todo check if database is empty
    # records who havent been climbed $1 offset $2 limit
    rows = conn.query(Users).filter(Users.fr_status == 0).all()[1:8]

    myQueue = queue.Queue()

    for row in rows:
        myQueue.put(row)

    while(myQueue.qsize()):
        tasks = []
        # thread number
        for i in range(0, 10):
            Thread = MyClimberThread(i, connection=conn, queue=myQueue)
            Thread.setDaemon(False)
            Thread.start()
            tasks.append(Thread)

        for task in tasks:
            if task.isAlive():
                tasks.append(task)
            continue




