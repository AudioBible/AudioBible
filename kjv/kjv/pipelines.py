# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import urllib2
from urlparse import urlparse
from scrapy import signals
from scrapy.exporters import BaseItemExporter, JsonLinesItemExporter
from .settings import DATA_STORE, URLS_FILE


if not os.path.isdir('%s/' % DATA_STORE):
    os.makedirs('%s/' % DATA_STORE)


class FileExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file

    def export_item(self, data):
        self.file.write(data)


class KjvPipeline(FileExporter):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    def process_item(self, item, spider):
        if item and \
                'book' in item.keys() and \
                'text' in item.keys() and \
                'url' in item.keys():
            _book = item['book'].split(' ')
            book_name = " ".join(_book[:-1])
            if not os.path.isdir('%s/%s/' % (DATA_STORE, book_name)):
                os.makedirs('%s/%s/' % (DATA_STORE, book_name))

            filename = '%s/%s/%s.txt' % (DATA_STORE, book_name, item['book'].replace(' ', '_').lower())
            if not os.path.exists(filename):
                chapter_file = open(filename, 'w')
                self.files[spider] = chapter_file
                self.exporter = FileExporter(chapter_file)
                self.exporter.start_exporting()
                self.exporter.export_item("\n".join(item['text']))
                self.exporter.finish_exporting()
                chapter_file = self.files.pop(spider)
                chapter_file.close()
        if item and \
                'name' in item.keys() and \
                'urls' in item.keys():
            found_in_bible_file = False
            if os.path.exists(URLS_FILE):
                with open(URLS_FILE, 'rw') as bible:
                    for books in bible:
                        if item['name'] in books:
                            found_in_bible_file = True

                            break
            if not found_in_bible_file:
                bible_file = open(URLS_FILE, 'a+')
                self.files[spider] = bible_file
                self.exporter = JsonLinesItemExporter(bible_file)
                self.exporter.start_exporting()
                self.exporter.export_item(item)
                self.exporter.finish_exporting()
                chapter_file = self.files.pop(spider)
                chapter_file.close()
        return item


class Mp3Pipeline(FileExporter):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    def process_item(self, item, spider):
        if item and \
                'book' in item.keys() and \
                'mp3' in item.keys() and \
                'url' in item.keys():
            _book = item['book'].split(' ')
            book_name = " ".join(_book[:-1])
            filename = urlparse(item['mp3']).path.split('/')[-1]
            if not os.path.isdir('%s/%s/' % (DATA_STORE, book_name)):
                os.makedirs('%s/%s/' % (DATA_STORE, book_name))

            download_path = '%s/%s/%s' % (DATA_STORE, book_name, filename)

            if not os.path.exists(download_path):
                req = urllib2.Request(item['mp3'])
                req.add_header('Referer', '%s' % item['url'])
                r = urllib2.urlopen(req)

                mp3_file = open(download_path, 'wb')

                self.files[spider] = mp3_file
                self.exporter = FileExporter(mp3_file)
                self.exporter.start_exporting()
                self.exporter.export_item(r.read())
                self.exporter.finish_exporting()
                chapter_file = self.files.pop(spider)
                chapter_file.close()
        return item