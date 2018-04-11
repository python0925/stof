# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,MapCompose
from scrapy.spiders import CrawlSpider, Rule

from stackoverflow.items import StackoverflowItem


class StofSpider(CrawlSpider):
    name = 'stof'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?sort=votes&pageSize=50']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pager fl"]/a[contains(@rel,"next")]')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="summary"]/h3/a'),callback='parse_item'),

    )

    def parse_item(self, response):
        i = StackoverflowItem()
        l = ItemLoader(item=i,response=response)
        l.default_output_processor = Join('')
        l.add_xpath('title','//div[@id="question-header"]/h1/a/text()')
        l.add_xpath('question','//div[contains(@class,"postcell")]/div//p/text()',MapCompose(lambda s:s.replace('\n',"")))
        l.add_xpath('answers','//div[contains(@class,"answercell")]/div//p/text()',MapCompose(lambda s:s.replace('\n',"")))
        yield l.load_item()
