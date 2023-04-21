import os
import pickle
import time
from selenium.webdriver.chrome import service
from selenium import webdriver


def get_cookie_from_network():
    # 这个url比较关键，网络上比较老的办法是
    # url_login = 'https://login.taobao.com/member/login.jhtml'
    # 测试之后发现，会报错“可能不是一个可交互的element”
    # 在后面添加?style=mini后就可以了
    url_login = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=&city=101010100&experience=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30'
    # 这一段是为了给selenium添加user-agent。模拟浏览器
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get(url_login)
    print()
    # driver.find_element_by_id("J_Static2Quick").click()

    # 获得 cookie信息
    cookie_list = driver.get_cookies()
    print(cookie_list)

    cookie_dict = {}
    for cookie in cookie_list:
        # 写入文件
        f = open('cookies/' + cookie['name'] + '.taobao', 'w')
        pickle.dump(cookie, f)
        f.close()

        if cookie.has_key('name') and cookie.has_key('value'):
            cookie_dict[cookie['name']] = cookie['value']

    return cookie_dict

if __name__ == '__main__':
    get_cookie_from_network()