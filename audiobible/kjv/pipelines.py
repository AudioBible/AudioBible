# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
from scrapy import signals
from scrapy.exporters import BaseItemExporter, JsonLinesItemExporter

try:
    from urllib2 import urlopen
    from urllib2 import Request
    from urlparse import urlparse
except:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.parse import urlparse


class FileExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file

    def export_item(self, data):
        self.file.write(data)


def get_book_name(item):
    return "_".join(item['book'].split(' ')[:-1])


def get_filename(item, ext):
    mp3 = urlparse(item['mp3'].replace('.mp3', '')).path.split('/')[-1].split('_')
    num = '%02d' % int(mp3[0])
    name = mp3[1].upper()
    try:
        chapter = '%s' % int(mp3[2])
    except IndexError:
        chapter = 1
    return "_".join([name, '%s.%s' % (chapter, ext)]).replace('-', '_')


def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


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
        DATA_STORE = spider.settings.get('DATA_STORE')
        if item and \
                'book' in item.keys() and \
                'text' in item.keys() and \
                'mp3' in item.keys() and \
                'url' in item.keys():
            book_name = get_book_name(item)

            ensure_dir(os.path.join(DATA_STORE, book_name))

            filename = os.path.join(DATA_STORE, book_name, get_filename(item, 'txt'))
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
            CONTENT_FILE = os.path.join(DATA_STORE, spider.settings.get('CONTENT_FILE'))
            if os.path.exists(CONTENT_FILE):
                with open(CONTENT_FILE, 'r') as bible:
                    for books in bible:
                        if item['name'] in books:
                            found_in_bible_file = True

                            break
            else:
                ensure_dir('%s' % DATA_STORE)

            if not found_in_bible_file:
                bible_file = open(CONTENT_FILE, 'a+')
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
        DATA_STORE = spider.settings.get('DATA_STORE')
        if item and \
                'book' in item.keys() and \
                'mp3' in item.keys() and \
                'url' in item.keys():
            book_name = get_book_name(item)

            ensure_dir(os.path.join(DATA_STORE, book_name))

            download_path = os.path.join(DATA_STORE, book_name, get_filename(item, 'mp3'))

            if not os.path.exists(download_path):
                req = urllib2.Request(item['mp3'])
                req.add_header('Referer', '%s' % item['url'])
                r = urlopen(req)

                mp3_file = open(download_path, 'wb')

                self.files[spider] = mp3_file
                self.exporter = FileExporter(mp3_file)
                self.exporter.start_exporting()
                self.exporter.export_item(r.read())
                self.exporter.finish_exporting()
                chapter_file = self.files.pop(spider)
                chapter_file.close()
        return item
