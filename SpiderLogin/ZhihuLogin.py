"""这是一个模拟知乎的程序"""
import requests
from lxml import etree
import time

loginurl = "https://www.zhihu.com/login/phone_num"      #知乎手机登录


data = {
        'phone_num':'*****',            #你的手机号
        'password':'*****',             #你的密码
        'remember_me': 'true'
       }

header = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0',
                'Accept':'*/*',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Referer':'https://www.zhihu.com/',
                'Accept-Encoding':'gzip, deflate, br',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
         }                   #用firefoxhttp取得header和data，两个是登录请求的信息千万别弄错！


S = requests.session()      #保持session

#下载验证码
def DownloadImg():
    t = str(int(time.time() * 1000))        #验证码图片是根据时间生成的，加入链接就是图片地址
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = S.get(captcha_url, headers=header)
    with open('验证码.jpg','wb') as f:                 #下载图片
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


#data中必须要有的内容，每次登录都不一样
def get_xsrf():
    r = requests.get(loginurl,headers = header).content
    page = etree.HTML(r)
    info = page.xpath(u'//div[@class="view view-signin"]/form/input[@type="hidden"]')
    xsrf = info[0].values()[2]
    return xsrf


#模拟登录
def Login():
    data['_xsrf'] = get_xsrf()
    capha = input('请输入验证码:')
    data['captcha'] = capha         #验证码下载在本地，用户需打开图片输入验证码
    index = S.post(loginurl, data = data, headers = header)
    login_code = eval(index.text)
    print(login_code['msg'])        #获取登录状态


if __name__=='__main__':
    DownloadImg()
    Login()

