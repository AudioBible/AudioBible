# -*- coding: utf-8 -*-
import scrapy
import os
import json
import string
from ..items import get_item_and_loader

from scrapy.utils.project import get_project_settings as Settings
settings = Settings()


class TopicsSpider(scrapy.Spider):
    name = "topics"
    allowed_domains = ["www.sermonaudio.com"]

    def __init__(self):
        self.start_urls = ["http://www.sermonaudio.com/sermonstopic.asp"]

    def parse(self, response):
        if response.status in (200, ):
            item, loader = get_item_and_loader('Topics', keys=[
                'name',
                'url',
                'letter'
            ])
            l = loader(response=response)
            names = l.get_xpath('//a[contains(@class, "navleftblack2b")][contains(@href, "sermonstopic")]/*/text()')
            urls = l.get_xpath('//a[contains(@class, "navleftblack2b")][contains(@href, "sermonstopic")]/@href')
            for n in range(len(names)):
                itm = item()
                itm['name'] = u"".join(names[n]).strip()
                itm['url'] = u"".join(urls[n]).strip()
                itm['letter'] = u"".join(names[n]).strip()[0].upper()

                li = loader(item=itm)
                yield li.load_item()
