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
    hebrew_count = 8674

    def __init__(self):
        [self.start_urls.append("%sH%s" % (self.strongs_url, i)) for i in range(1, self.hebrew_count + 2)]
        [self.start_urls.append("%sG%s" % (self.strongs_url, i)) for i in range(1, self.greek_count + 2)]

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
                'brown_driver_definition',
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
                        "Definitions": []
                    }
                    _texts = l.get_xpath('%s/p' % text_path)
                    for tdx in range(1, len(_texts) + 1):
                        data = " ".join(l.get_xpath(
                            '%s[%s]/p[%s]/text()|%s[%s]/p[%s]/*/text()' % (text_path, wdx, tdx, text_path, wdx, tdx)
                        ))
                        if len(data.strip()) > 0:
                            item['data'][wdx]['Definitions'].append(data.strip())
                yield item
            else:
                loc = urlparse(response.url).path.strip('/').split('/')
                if len(loc) > 2:
                    if 'item' in response.meta:
                        itm = response.meta['item']
                        bible_refs = l.get_xpath(
                            '//td[contains(text(), "Bible References")]/following-sibling::td/*/a/text()'
                        )
                        itm['bible_references'] = list(itm['bible_references']) + bible_refs
                    else:
                        itm['strongs_number'] = u"".join(l.get_xpath(
                            '//td[contains(text(), "Strong\'s No.:")]/following-sibling::td/text()'
                        ))
                        if 'No/H' in response.url:
                            itm['word_original'] = u"".join(l.get_xpath(
                                '//td[contains(text(), "Hebrew:")]/following-sibling::td/text()'
                            )).encode('utf-8')
                        elif 'No/G' in response.url:
                            itm['word_original'] = u"".join(l.get_xpath(
                                '//td[contains(text(), "Greek:")]/following-sibling::td/text()'
                            )).encode('utf-8')
                        itm['word_translated'] = urlparse(response.url).path.strip('/').split('/')[2]
                        itm['letter'] = itm['word_translated'][0].upper()

                        itm['transliteration'] = u"".join(l.get_xpath(
                            '//td[contains(text(), "Transliteration:")]/following-sibling::td/text()'
                        )).encode('utf-8')
                        itm['phonetic'] = u"".join(l.get_xpath(
                            '//td[contains(text(), "Phonetic:")]/following-sibling::td/text()'
                        ))
                        path = '//td[contains(text(), "Word Origin:")]/following-sibling::td'
                        itm['word_origin'] = u"".join(l.get_xpath(
                            '%s/text()|%s/a/text()' % (path, path)
                        ))
                        itm['origin_links'] = l.get_xpath(
                            '//*[contains(text(), "Word Origin:")]/following-sibling::td/a/@target'
                        )
                        itm['bible_usage'] = u"".join(l.get_xpath(
                            '//*[contains(text(), "Bible Usage:")]/following-sibling::td/text()'
                        ))
                        itm['part_of_speech'] = u"".join(l.get_xpath(
                            '//*[contains(text(), "Part of Speech:")]/following-sibling::td/text()'
                        ))
                        path = '//td[contains(@class, "stgfcol")]/*[contains(text(), "Strong")]/parent::*/following-sibling::td'
                        itm['strongs_definition'] = u"".join(l.get_xpath(
                            '%s/text()|%s/*/text()' % (path, path)
                        ))
                        path ='//td/*[contains(text(), "Brown Driver")]/parent::*/following-sibling::td'
                        itm['brown_driver_definition'] = l.get_xpath(
                            '%s/*/text()|%s/*/*/text()' % (path, path)
                        )
                        path = '//td/*[contains(text(), "Thayers")]/parent::*/following-sibling::td'
                        itm['thayers_definition'] = l.get_xpath(
                            '%s/*/text()|%s/*/*/text()' % (path, path)
                        )
                        names = [n.strip('/').split('/')[2] for n in l.get_xpath(
                            '//td[contains(text(), "Translation")]/following-sibling::td/div/a/@href'
                        )]
                        itm['translation_occurrences'] = dict(zip(
                            names,
                            l.get_xpath(
                                '//td[contains(text(), "Translation")]/following-sibling::td/*/strong/text()'
                            )
                        ))

                        itm['bible_references'] = l.get_xpath(
                            '//td[contains(text(), "Bible References")]/following-sibling::td/*/a/text()'
                        )

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
                    urls = l.get_xpath('//td[contains(text(), "Translation")]/following-sibling::td/*/a/@href')
                    for url in [urljoin(response.url, x) for x in urls]:
                        yield Request(url, callback=self.parse)
