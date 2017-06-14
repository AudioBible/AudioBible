# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import Crawler
import os
import json
from ..items import get_item_and_loader

from scrapy.utils.project import get_project_settings as Settings
settings = Settings()


class BibleSpider(scrapy.Spider):
    name = "bible"
    allowed_domains = ["www.audiobible.com"]
    start_urls = []

    def __init__(self, data_store=settings.get('DATA_STORE'), content_file=settings.get('CONTENT_FILE')):
        p = os.path.join(data_store, content_file)
        if os.path.exists(p) and not os.stat(p).st_size == 0:
            with open(os.path.join(data_store, content_file)) as f:
                for line in f.readlines():
                    data = json.loads(line)
                    if data['urls']:
                        for url in data['urls']:
                            self.start_urls.append(url)
        else:
            self.start_urls.append('http://www.audiobible.com/bible/bible.html')

    def parse(self, response):
        if response.status in (200, ):
            if '/bible.html' in response.url:
                item, loader = get_item_and_loader('Bible', keys=[
                    'name',
                    'chapters_count',
                    'urls',
                ])
                l = loader(response=response)
                names = l.get_xpath('//div[contains(@class, "PageContent")]//span[contains(@class, "aname")]/text()')
                chapters = l.get_xpath('//div[contains(@class, "PageContent")]//li[last()]/a/text()')
                urls = l.get_xpath('//div[contains(@class, "PageContent")]//li[last()]/a/@href')

                for n in range(len(names)):
                    itm = item()
                    itm['name'] = names[n].strip()
                    chapters_count = int(chapters[n].strip())
                    itm['chapters_count'] = chapters_count
                    urls_list = []
                    for u in range(1, chapters_count + 1):
                        chapter_url = urls[n].replace('%s.html' % chapters_count, '%s.html' % u)
                        urls_list.append(chapter_url)
                    itm['urls'] = urls_list
                    li = loader(item=itm)
                    yield li.load_item()
            else:
                item, loader = get_item_and_loader('Bible', keys=[
                    'book',
                    'text',
                    'mp3',
                    'url'
                ])
                l = loader(response=response)
                itm = item()
                book = "".join(l.get_xpath('//h1/text()'))
                itm['book'] = book.upper()
                itm['text'] = l.get_xpath('//div[contains(@class, "PageContent")]//strong/text()')
                mp3 = "".join(l.get_xpath('//object/@data')).split('niftyplayer.swf?file=')[1].replace('&as=1', '')
                itm['mp3'] = mp3
                itm['url'] = response.url
                li = loader(item=itm)
                yield li.load_item()
