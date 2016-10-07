"""这是一个模拟登录豆瓣的程序"""
import requests
from lxml import etree

loginurl = "https://www.douban.com/accounts/login"

data = {
        "redir":"https://www.douban.com",
        "form_email":"******",                 #输入你的豆瓣帐号
        "form_password":"******",              #输入你的豆瓣密码
       }

header = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Host':'accounts.douban.com'
         }                   #用firefoxhttp取得header和data，两个是登录请求的信息


#下载验证码
def DownloadJpg():
    page = requests.get(loginurl)
    if "请输入上图中的单词" in page.text:
        html = page.content
        index = etree.HTML(html)
        url = index.xpath(u'//img[@id="captcha_image"]')
        Url = url[0].values()[1]
        Id = index.xpath(u'//div[@class="captcha_block"]/input[@type="hidden"]')
        id = Id[0].values()[2]
        I = requests.get(Url,stream=True)
        with open('验证码.jpg','wb') as f:                 #下载图片
                for chunk in I.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        return id
    return 0        #如果需要验证码就返回验证码id，不需要返回0


#模拟登录
def Login01(id):
    s = requests.session()
    if id != 0:             #需要验证码就添加验证码信息
        captcha = input("请输入目录下的验证码(请等待10秒验证码图片下载):")
        data['captcha-solution'] = captcha
        data['captcha-id'] = id
    l = s.post(loginurl, data = data, headers = header)
    if '的帐号' in l.text:         #判断登录是否成功
        print('登陆成功')
    else:
        print('登录失败')


#用cookie模拟登录，待完善！！！
def Login02(id):
    req = requests.session()
    cookie = {}
    cookies = ''
    for line in cookies.split(';'):
        key,value = line.split('=',1)   #1代表只分一次，得到两个数据
        cookie[key] = value
    s = req.get(loginurl,cookies = cookie)
    print(s.text)


if __name__=='__main__':
    id = DownloadJpg()
    Login01(id)
