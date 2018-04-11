# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random

import requests
from requests.exceptions import ConnectionError
from scrapy.exceptions import IgnoreRequest




class ProxyMiddleware(object):

    def __init__(self,proxy_pool_url,user_agent):
        self.logger = logging.getLogger(__name__)
        self.proxy_pool_url = proxy_pool_url
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            proxy_pool_url = crawler.settings.get('PROXY_POOL_URL'),
            user_agent = crawler.settings.get('UA')
        )

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_pool_url)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            return None

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        self.logger.debug(response.status)
        if response.status != 200:
            proxy = self.get_proxy()
            self.logger.debug("this is request ip:" + proxy)
            request.meta['proxy'] = 'http://' + proxy
            agent = random.choice(self.user_agent)
            request.headers['User-Agent'] = agent
            request.headers.setdefault('Referrer', 'https://stackoverflow.com')
            self.logger.debug(request.headers)
            return request
        return response



