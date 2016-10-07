"""这是一个模拟登录微博的程序,其中data里面的su,sp,servicetime,nonce,raskv是动态获取"""
import requests
from lxml import etree
import json
import re
import base64
import rsa, binascii

loginurl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)" #要登录的网址
username = "*******"        #你的帐号
password = "*******"        #你的密码

data = {
        'entry':'weibo',
        'gateway':'1',
        'from':'',
        'savestate':'7',
        'useticket':'1',
        'pagerefer': 'http://weibo.com/signup/signup.php?inviteCode=3504310343',
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
        'prelt':'95',
        'url':'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)',
        'returntype' : 'META'
        }

header = {
        'Host': 'login.sina.com.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Referer':'http://weibo.com/',
        'Content-Type':'application/x-www-form-urlencoded'
        }
        #data和header是由firefoxhttp取得

S = requests.session()

#获得由rsa加密过的密码
def getPassword(password):
    rsaPublickey = int(data['pubkey'], 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    message = data['servertime'] + '\t' + data['nonce'] + '\n' + str(password)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    passwd = binascii.b2a_hex(passwd)
    return passwd


#获取base64加密的用户名
def getUsername(username):
    Username = base64.b64encode(username.encode('utf-8'))
    return Username.decode()


#取得js页面中的4个动态信息，并登录
def Login01():
    url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=ZW5nbGFuZHNldSU0MDE2My5jb20%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1442991685270"
    info = S.get(url)
    p = re.search('[^(（]+(?=[)）])',info.text).group(0)
    a = json.loads(p)
    data['servertime'] = str(a['servertime'])
    data['rsakv'] = a['rsakv']
    data['nonce'] = a['nonce']
    data['pubkey'] = a['pubkey']
    data['su'] = getUsername(username)
    data['sp'] = getPassword(password).decode()
    index = S.post(loginurl,data = data,headers = header)
    if "Signing in ..." in index.text:
        print('登陆成功')
    else:
        print('登录失败')


if __name__ == '__main__':
    Login01()




