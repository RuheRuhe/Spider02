"""模拟登录豆瓣"""
import requests
from lxml import etree


header = {
    'Host':'accounts.douban.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate, br',
    'Referer':'https://www.douban.com/accounts/login',
    'Content-Type':'application/x-www-form-urlencoded',
    'Content-Length':'126'
}

data= {
    'redir':'https://www.douban.com',
    'form_email':'',
    'form_password':''
}
#data和header由谷歌浏览器获得

#用户输入用户名和密码登录豆瓣
def Login01(url,username,pwd):
    data['form_email'] = username
    data['form_password'] = pwd
    s = requests.Session()
    text = s.get(url).text
    if '请输入上图中的单词' in text:     #如果有验证码
        page = etree.HTML(text)
        img = page.xpath('//img[@id="captcha_image"]/@src')     #取得验证码图片
        id = page.xpath('//div[@class="captcha_block"]/input[@type="hidden"]/@value')   #取得登录必需的验证码值
        pic = requests.get(img[0])
        with open('豆瓣验证码','wb') as f:
            for chunk in pic.iter_content(1024):
                if chunk:
                    f.write(chunk)
        captcha = input('请输入验证码:')
        data['captcha-solution'] = captcha
        data['captcha-id'] = id[0]
    p = s.post(url,headers=header,data=data)
    if '的帐号' in p.text:
        print('登录成功')
    else:
        print('登录失败')


if __name__ == '__main__':
    url = "https://www.douban.com/accounts/login"
    username = input('请输入用户名:')
    pwd = input('请输入密码:')
    Login01(url,username,pwd)

