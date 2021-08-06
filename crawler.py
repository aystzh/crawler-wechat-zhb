import json
from selenium import webdriver
import time
import requests


def weChat_login(user, password):
    post = {}
    browser = webdriver.Chrome("./chromedriver")
    browser.get('https://mp.weixin.qq.com/')
    time.sleep(3)
    browser.delete_all_cookies()
    time.sleep(2)
    # 点击切换到账号密码输入
    browser.find_element_by_xpath(
        "//a[@class='login__type__container__select-type']").click()
    time.sleep(2)
    # 模拟用户点击
    input_user = browser.find_element_by_xpath("//input[@name='account']")
    input_user.send_keys(user)
    input_password = browser.find_element_by_xpath("//input[@name='password']")
    input_password.send_keys(password)
    time.sleep(2)
    # 点击登录
    browser.find_element_by_xpath("//a[@class='btn_login']").click()
    time.sleep(2)
    # 微信登录验证
    print('请扫描二维码')
    time.sleep(20)
    # 刷新当前网页
    browser.get('https://mp.weixin.qq.com/')
    time.sleep(5)
    # 获取当前网页链接
    url = browser.current_url
    # 获取当前cookie
    cookies = browser.get_cookies()
    for item in cookies:
        post[item['name']] = item['value']
    # 转换为字符串
    cookie_str = json.dumps(post)
    # 存储到本地
    with open('cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print('cookie保存到本地成功')
    # 对当前网页链接进行切片，获取到token
    paramList = url.strip().split('?')[1].split('&')
    # 定义一个字典存储数据
    paramdict = {}
    for item in paramList:
        paramdict[item.split('=')[0]] = item.split('=')[1]
    # 返回token
    return paramdict['token']


def crawler_wx():
    token = weChat_login("xxx@163.com", "xxx")
    url = 'https://mp.weixin.qq.com'
    headers = {
        'HOST': 'mp.weixin.qq.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
    }
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    resp = requests.get(url=url, headers=headers, cookies=cookies)
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    params = {
        'action': 'search_biz',
        'begin': '0',
        'count': '5',
        'query': '中华保险',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1'
    }
    search_resp = requests.get(
        url=search_url, cookies=cookies, headers=headers, params=params)
    lists = search_resp.json().get('list')[0]
    fakeid = lists.get('fakeid')
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    params_data = {
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'fakeid': fakeid,
        'type': '9',
        'query': '',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1'
    }
    appmsg_resp = requests.get(
        url=appmsg_url, cookies=cookies, headers=headers, params=params_data)
    print(appmsg_resp.text)
    return appmsg_resp


if __name__ == '__main__':
    msg = crawler_wx()
    #print(msg.text)
