import time

import scrapy
import json
import logging
import random
from bosszp.items import BosszpItem
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/wapi/zpCommon/data/cityGroup.json']
    # 设置多个 cookie,建议数量为 页数/2 + 1 个cookie.至少 设置 4 个
    # 只需复制 __zp_stoken__ 部分即可
    cookies = [
        'wd_guid=0af9d2c7-8f7e-4612-8ea7-ba2b1b91b05e; historyState=state; _bl_uid=9dlXLewI4786IwwC0gsk0Omhe01a; lastCity=100010000; wt2=D4nBd99oNUpM_32Wq3BPub4RlLBSGHYLkFo9XFr8OF3aPrxmVOpapLk9QmU9fPhwiNTQXBHku-W2xw880BXr4IA~~; wbg=0; __g=-; __c=1678964415; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __a=14193959.1676375853.1678964296.1678964415.442.28.2.442; __zp_stoken__=5f92eWDhxLE5TMT8IWiJhYSBdIAASeF5tPWxtN2wrN2hXXH0TKARwFBx2QToNH2lrfR9fXn0YRwNIBj5kFzFZXXtvLA1gZi1HV14yKyg7WA9JeEojbWUiGSNOEmJrTRxxPyZtP31nRXQKOiU%3D; geek_zp_token=V1RNkmF-T53FduVtRvyBURLy-56jPRxyg~'
    ]
    # 设置多个请求头
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    ]
    page_no = 1  # 初始化分页

    # def get_cookies(self):
    #     service = Service('chromedriver.exe')
    #     option = webdriver.ChromeOptions()
    #     option.add_experimental_option('debuggerAddress', 'localhost:9222')
    #     # option.add_experimental_option('excludeSwitches',['enable-automation'])
    #     driver = webdriver.Chrome(options=option, service=service)
    #     driver.get('https://www.zhipin.com/web/geek/job?city=100010000')
    #     time.sleep(10)
    #     list = driver.get_cookies()
    #     dict = {i['name']: i['value'] for i in list}
    #     cookies = str(dict).replace(': ', '=').replace('\'', '').replace(',', ';').replace('{','').replace('}','')
    #     driver.quit()
    #     return cookies


    def random_header(self):
        """
        随机生成请求头
        :return: headers
        """
        headers = {'Referer': 'https://www.zhipin.com/web/geek/job?query='}
        headers['cookie'] =random.choice(self.cookies)
        headers['user-agent'] = random.choice(self.user_agents)
        return headers

    def parse(self, response):
        """
        解析首页热门城市列表，选择热门城市进行爬取
        :param response: 热门城市字典数据
        :return:
        """
        # 获取服务器返回的内容
        city_group = json.loads(response.body.decode())
        # 获取热门城市列表
        hot_city_list = city_group['zpData']['hotCityList']
        # 初始化空列表，存储打印信息
        # city_lst = []
        # for index,item in enumerate(hot_city_list):
        #    city_lst.apend({index+1: item['name']})
        # 列表推导式：
        hot_city_names = [{index + 1: item['name']} for index, item in enumerate(hot_city_list)]
        print("--->", hot_city_names)
        # 从键盘获取城市编号
        city_no = int(input('请从上述城市列表中，选择编号开始爬取：'))
        kw = input('请输入搜索关键词：')
        # 拼接url https://www.zhipin.com/job_detail/?query=&city=101040100&industry=&position=
        # 获取城市编码code
        city_code = hot_city_list[city_no - 1]['code']
        city_url = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query={}&city={}&page='.format(kw,city_code)
        self.start_urls = city_url
        logging.info("<<<<<<<<<<<<<正在爬取第_{}_页岗位数据>>>>>>>>>>>>>".format(self.page_no))
        # print(self.random_header())
        yield scrapy.Request(url=city_url, headers=self.random_header(), callback=self.parse_city)

    def parse_city(self, response):

        """
        解析岗位页数据
        :param response: 岗位页响应数据
        :return:
        """
        if response.status != 200:
            logging.warning("<<<<<<<<<<<<<获取城市招聘信息失败，ip已被封禁。请稍后重试>>>>>>>>>>>>>")
            return
        data = json.loads(response.body.decode())

        try:
            li_elements = json.loads(response.text)['zpData']['jobList']
        except:
            return
            # print('cookie失效 ，重新获取请求头！')
            # self.random_header()
            # next_url = self.start_urls.replace('page=', 'page=' + str(self.page_no))
            # print(next_url)
            # logging.info("<<<<<<<<<<<<<正在爬取第_{}_页岗位数据>>>>>>>>>>>>>".format(self.page_no))
            # yield scrapy.Request(url=next_url, headers=self.random_header(), callback=self.parse_city)
            # return

        for li in li_elements:
            job_name = li['jobName']
            seq = (li['cityName'],li['cityName'],li['businessDistrict'])
            job_area = '·'.join(seq)
            job_salary = li['salaryDesc']
            com_name = li['brandName']
            com_type = li['brandIndustry']
            com_size = li['brandScaleName']
            finance_stage = li['brandStageName']
            work_year = li['jobLabels'][0]
            education = li['jobLabels'][1]
            job_benefits = str(li['welfareList']).replace('\'','').replace('[','').replace(']','').replace(',','、')
            item = BosszpItem(job_name=job_name, job_area=job_area, job_salary=job_salary, com_name=com_name,
                              com_type=com_type, com_size=com_size,
                              finance_stage=finance_stage, work_year=work_year, education=education,
                              job_benefits=job_benefits)
            yield item
        self.page_no += 1
        if self.page_no >10:
            print(self.page_no)
            return
        next_url = self.start_urls.replace('page=','page='+str(self.page_no))
        print(next_url)
        logging.info("<<<<<<<<<<<<<正在爬取第_{}_页岗位数据>>>>>>>>>>>>>".format(self.page_no))
        yield scrapy.Request(url=next_url, headers=self.random_header(), callback=self.parse_city)
