import requests
from lxml import etree
import re
import json
import base64
import rsa,binascii
import time

S = requests.session()

loginurl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"

header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'login.sina.com.cn',
    'Origin':'http://weibo.com',
    'Referer':'http://weibo.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
}

data = {
    'entry':'weibo',
    'gateway':'1',
    'savestate':'7',
    'useticket':'1',
    'pagerefer':'http://weibo.com/u/3504310343/home',
    'vsnf':'1',
    'su':'',
    'service':'miniblog',
    'servertime':'',
    'nonce':'',
    'pwencode':'rsa2',
    'rsakv':'',
    'sp':'',
    'sr':'1366*768',
    'encoding':'UTF-8',
    'prelt':'761',
    'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype':'META'
}

def getInfo():
    url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=ZW5nbGFuZHNldSU0MDE2My5jb20%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1442991685270"
    text = S.get(url).text
    info = re.compile(r'({.*})')
    Info = info.search(text).group(0)
    i = json.loads(Info)
    data['servertime'] = str(i['servertime'])
    data['rsakv'] = i['rsakv']
    data['nonce'] = i['nonce']
    data['pubkey'] = i['pubkey']


def getUsername(username):
    username = username.replace('@','%40')
    Username = base64.b64encode(username.encode('utf-8'))
    return Username.decode()


def getPwd(pwd):
    rsaPublickey = int(data['pubkey'], 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    message = data['servertime'] + '\t' + data['nonce'] + '\n' + str(pwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    passwd = binascii.b2a_hex(passwd)
    return passwd


def Login01():
    username = '763242665@qq.com'
    password = 'ifp==null'
    index = S.post(loginurl,headers=header,data=data)
    data['su'] = getUsername(username)
    data['sp'] = getPwd(password).decode()
    print(index.text)


if __name__ == '__main__':
    getInfo()
    print(data)
    Login01()