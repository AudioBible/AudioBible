# -*- coding: utf-8 -*-
import scrapy
import os
import json
import string
from ..items import get_item_and_loader

from scrapy.http import Request
from scrapy.utils.project import get_project_settings as Settings
settings = Settings()


class DictionarySpider(scrapy.Spider):
    name = "dictionary"
    allowed_domains = ["www.biblestudytools.com"]

    def __init__(self):
        self.start_urls = ["http://www.biblestudytools.com/dictionaries/king-james-dictionary/?letter=%s" % l for l in list(string.ascii_uppercase) if l != 'x' and l != 'z']

    def parse(self, response):
        if response.status in (200, ):
            item, loader = get_item_and_loader('Dictionary', keys=[
                'letter',
                'word',
                'link',
                'description',
                'definition',
                'scriptures'
            ])
            if 'letter=' in response.url:
                l = loader(response=response)
                part = '//li[contains(@class, "list-group-item")][not(contains(@class, "close"))]'
                part += '[not(contains(@class, "inverse"))]/a'
                links = l.get_xpath('%s/@href' % part)

                for n in range(len(links)):
                    letter = u"".join(response.url.split('letter=')[1].upper())
                    url = u"".join(links[n]).strip()
                    yield Request(url=url, callback=self.parse, meta={'letter': letter})
            else:
                itm = item()
                l = loader(response=response)
                itm['letter'] = response.meta['letter']
                itm['word'] = "".join(l.get_xpath('//article[@class="library"]/font[1]/b/text()'))
                itm['description'] = "".join(l.get_xpath('//article[@class="library"]/blockquote/i/text()'))
                definition = '//article[@class="library"]/blockquote/p/text()'
                definition += '|//article[@class="library"]/blockquote/p/b/font/text()'
                verses = '//article[@class="library"]/blockquote/p/a/text()'
                definition += '|%s' % verses
                itm['definition'] = "".join(l.get_xpath(definition))
                itm['scriptures'] = l.get_xpath(verses)
                itm['link'] = response.url
                li = loader(item=itm)
                yield li.load_item()
