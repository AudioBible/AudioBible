# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import json
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
                req = Request(item['mp3'])
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


class SpeakerPipeline(FileExporter):
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
                'name' in item.keys() and \
                'path' in item.keys() and \
                'letter' in item.keys():
            found_in_speaker_file = False
            SPEAKERS_FILE = os.path.join(DATA_STORE, spider.settings.get('SPEAKERS_FILE') % item['letter'])
            if os.path.exists(SPEAKERS_FILE):
                with open(SPEAKERS_FILE, 'r') as speakers:
                    for speaker in speakers:
                        if item['name'] in speaker:
                            found_in_speaker_file = True

                            break
            else:
                ensure_dir('%s' % os.path.dirname(SPEAKERS_FILE))

            if not found_in_speaker_file:
                speakers_file = open(SPEAKERS_FILE, 'a+')
                self.files[spider] = speakers_file
                self.exporter = JsonLinesItemExporter(speakers_file)
                self.exporter.start_exporting()
                self.exporter.export_item(item)
                self.exporter.finish_exporting()
                chapter_file = self.files.pop(spider)
                chapter_file.close()
        return item


class TopicPipeline(FileExporter):
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
                'name' in item.keys() and \
                'url' in item.keys() and \
                'letter' in item.keys():
            found_in_topic_file = False
            TOPICS_FILE = os.path.join(DATA_STORE, spider.settings.get('TOPICS_FILE') % item['letter'])
            if os.path.exists(TOPICS_FILE):
                with open(TOPICS_FILE, 'r') as topics:
                    for topic in topics:
                        if item['name'] in topic:
                            found_in_topic_file = True

                            break
            else:
                ensure_dir('%s' % os.path.dirname(TOPICS_FILE))

            if not found_in_topic_file:
                topics_file = open(TOPICS_FILE, 'a+')
                self.files[spider] = topics_file
                self.exporter = JsonLinesItemExporter(topics_file)
                self.exporter.start_exporting()
                self.exporter.export_item(item)
                self.exporter.finish_exporting()
                chapter_file = self.files.pop(spider)
                chapter_file.close()
        return item


class DictionaryPipeline(FileExporter):
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
                'letter' in item.keys() and \
                'strongs_number' in item.keys() and \
                'word_original' in item.keys() and \
                'word_translated' in item.keys():
            found_in_words_file = False

            language = 'all'
            if item['strongs_number'][0] == 'H':
                language = 'hebrew'
            elif item['strongs_number'][0] == 'G':
                language = 'greek'

            WORDS_FILE = os.path.join(DATA_STORE, spider.settings.get('DICTIONARY_FILE') % (language, item['letter']))
            if os.path.exists(WORDS_FILE):
                with open(WORDS_FILE, 'r') as words:
                    for word in words:
                        data = json.loads(word)
                        if item['word_translated'] == data['word_translated'] and \
                                item['strongs_number'] == data['strongs_number']:
                            found_in_words_file = True
                            break
            else:
                ensure_dir('%s' % os.path.dirname(WORDS_FILE))

            if not found_in_words_file:
                words_file = open(WORDS_FILE, 'a+')
                self.files[spider] = words_file
                self.exporter = JsonLinesItemExporter(words_file)
                self.exporter.start_exporting()
                self.exporter.export_item(item)
                self.exporter.finish_exporting()
                word_file = self.files.pop(spider)
                word_file.close()
        return item
