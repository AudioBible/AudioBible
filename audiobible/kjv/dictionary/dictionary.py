# -*- coding: utf-8 -*-
import scrapy
import os
import json
import string
try:
    from urlparse import urljoin, urlparse
except ImportError:
    from urllib.parse import urljoin, urlparse
from ..items import get_item_and_loader

from scrapy.http import Request
from scrapy.utils.project import get_project_settings as Settings
settings = Settings()


class DictionarySpider(scrapy.Spider):
    name = "dictionary"
    start_urls = []
    allowed_domains = ["www.kingjamesbibledictionary.com"]
    strongs_url = "http://www.kingjamesbibledictionary.com/StrongsNo/"
    greek_count = 5624
    hebrew_count = 8673

    def __init__(self):
        [self.start_urls.append("%sH%s" % (self.strongs_url, i)) for i in range(1, self.hebrew_count + 1)]
        [self.start_urls.append("%sG%s" % (self.strongs_url, i)) for i in range(1, self.greek_count + 1)]

    def parse(self, response):
        if response.status in (200, ):
            item, loader = get_item_and_loader('Dictionary', keys=[
                'letter',
                'strongs_number',
                'word_original',
                'word_translated',
                'transliteration',
                'phonetic',
                'word_origin',
                'origin_links',
                'bible_usage',
                'part_of_speech',
                'strongs_definition',
                'thayers_definition',
                'translation_occurrences',
                'bible_references',
                'data'
            ])

            itm = item()
            l = loader(response=response)

            if '/Dictionary/' in response.url:
                item = response.meta['item']
                item['data'] = {}

                names_path = '//div[contains(@class, "innercontainer")]/div[contains(@class, "defdct")]'
                words_path = '//div[contains(@class, "innercontainer")]/div[contains(@class, "defhd")]'
                _names = l.get_xpath('%s/text()' % names_path)
                _words = l.get_xpath('%s/text()' % words_path)

                text_path = '//div[contains(@class, "innercontainer")]/div[contains(@class, "deftxt")]'
                for wdx in range(1, len(_words) + 1):
                    item['data'][wdx] = {
                        "Dictionary": _names[wdx - 1],
                        "Word": _words[wdx - 1],
                        "Definition": "".join(l.get_xpath(
                            '%s[%s]/p/text()|%s[%s]/p/*/text()' % (text_path, wdx, text_path, wdx)
                        )),
                    }
                yield item
            else:
                table_xpath = '//table[contains(@class, "stgtable")]/'

                loc = urlparse(response.url).path.strip('/').split('/')

                if len(loc) > 2:
                    if 'item' in response.meta:
                        itm = response.meta['item']
                        bible_refs = l.get_xpath('%s/tr[19]/td[2]/div/a/text()' % table_xpath)
                        itm['bible_references'] = list(itm['bible_references']) + bible_refs
                    else:
                        itm['strongs_number'] = u"".join(l.get_xpath('%s/tr[1]/td[2]/text()' % table_xpath))
                        itm['word_original'] = u"".join(l.get_xpath('%s/tr[3]/td[2]/text()' % table_xpath))
                        itm['word_translated'] = urlparse(response.url).path.strip('/').split('/')[2]
                        itm['letter'] = itm['word_translated'][0].upper()
                        itm['transliteration'] = u"".join(l.get_xpath('%s/tr[5]/td[2]/text()' % table_xpath))
                        itm['phonetic'] = u"".join(l.get_xpath('%s/tr[7]/td[2]/text()' % table_xpath))
                        itm['word_origin'] = u"".join(l.get_xpath('%s/tr[9]/td[2]/text()|%s/tr[9]/td[2]/a/text()' % (
                            table_xpath, table_xpath
                        )))
                        itm['origin_links'] = l.get_xpath('%s/tr[9]/td[2]/a/@target' % table_xpath)
                        itm['bible_usage'] = u"".join(l.get_xpath('%s/tr[11]/td[2]/text()' % table_xpath))
                        itm['part_of_speech'] = u"".join(l.get_xpath('%s/tr[13]/td[2]/text()' % table_xpath))
                        itm['strongs_definition'] = u"".join(l.get_xpath('%s/tr[15]/td[2]/text()|%s/tr[15]/td[2]/*/text()' % (
                            table_xpath, table_xpath
                        )))
                        itm['thayers_definition'] = u"".join(l.get_xpath('%s/tr[17]/td[2]/text()|%s/tr[17]/td[2]/*/text()' % (
                            table_xpath, table_xpath
                        )))
                        names = [n.strip('/').split('/')[2] for n in l.get_xpath(
                            '%s/tr[21]/td[2]/*/a/@href|%s/tr[22]/td[2]/*/a/@href' % (table_xpath, table_xpath))
                        ]
                        itm['translation_occurrences'] = dict(zip(
                            names,
                            l.get_xpath('%s/tr[21]/td[2]/*/strong/text()|%s/tr[22]/td[2]/*/strong/text()' % (table_xpath, table_xpath))
                        ))

                        itm['bible_references'] = l.get_xpath('%s/tr[19]/td[2]/div/a/text()' % table_xpath)

                    li = loader(item=itm)

                    action = "".join(l.get_xpath('//div[contains(@class, "loadmore")]/form/@action'))

                    if action:
                        request = Request(urljoin(response.url, action), callback=self.parse)
                        request.meta['item'] = li.load_item()
                        yield request
                    else:
                        request = Request(
                            urljoin(response.url, '/Dictionary/%s' % itm['word_translated']),
                            callback=self.parse
                        )
                        request.meta['item'] = li.load_item()
                        yield request
                else:
                    urls = dict(zip(
                        l.get_xpath('%s/tr[19]/td[2]/*/a/@href' % table_xpath),
                        l.get_xpath('%s/tr[19]/td[2]/*/strong/text()' % table_xpath)
                    ))
                    for url in [urljoin(response.url, x) for x in urls.keys()]:
                        yield Request(url, callback=self.parse)
