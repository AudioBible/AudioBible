# -*- coding: utf-8 -*-
import scrapy
import os
import json
import string
from ..items import get_item_and_loader

from scrapy.utils.project import get_project_settings as Settings
settings = Settings()

# http://www.sermonaudio.com/sermonsspeaker.asp?localsection=A
# http://www.sermonaudio.com/search.asp?speakerWithinSource=&subsetCat=speaker&subsetItem=Rev+David+Silversides&mediatype=&includekeywords=&exactverse=&keyword=GENESIS&keyworddesc=Genesis+1&currsection=&AudioOnly=false&BibleOnly=true&Chapter=1&Verse=0


class SpeakersSpider(scrapy.Spider):
    name = "speakers"
    allowed_domains = ["www.sermonaudio.com"]

    def __init__(self):
        self.start_urls = ["http://www.sermonaudio.com/sermonsspeaker.asp?localsection=%s" % l for l in list(string.ascii_uppercase)]

    def parse(self, response):
        if response.status in (200, ):
            item, loader = get_item_and_loader('Speakers', keys=[
                'name',
                'path',
                'letter'
            ])
            l = loader(response=response)
            names = l.get_xpath('//a[contains(@class, "navleftblack2b")][contains(@href, "speaker/")]/text()')
            paths = l.get_xpath('//a[contains(@class, "navleftblack2b")][contains(@href, "speaker/")]/@href')
            for n in range(len(names)):
                itm = item()
                itm['name'] = u"".join(names[n]).strip()
                itm['path'] = u"".join(paths[n]).strip()
                itm['letter'] = u"".join(response.url.split('localsection=')[1].upper())

                li = loader(item=itm)
                yield li.load_item()
