#! /usr/bin/env python2

import re
import os
import sys
import json
import glob
import argparse
from scrapy.crawler import CrawlerProcess
from kjv.spiders.bible import BibleSpider
from kjv import settings

parser = argparse.ArgumentParser(
    prog='audiobible' or sys.argv[0],
    usage='%(prog)s operation [BOOK] [CHAPTER]',
    description='%(prog)s - King James Version Audio Bible')

parser.add_argument('operation', nargs='+', type=str, help="init, load, hear, read, find, list, quote, help")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

name = settings.BOT_NAME
data_path = os.path.join(os.path.expanduser('~'), settings.DATA_STORE)
content_path = os.path.join(data_path, settings.CONTENT_FILE)


class DownloadBible(object):
    @staticmethod
    def process():
        process = CrawlerProcess({
            'BOT_NAME': name,
            'SPIDER_MODULES': settings.SPIDER_MODULES,
            'NEWSPIDER_MODULE': settings.NEWSPIDER_MODULE,
            'USER_AGENT': settings.USER_AGENT,
            'ROBOTSTXT_OBEY': settings.ROBOTSTXT_OBEY,
            'ITEM_PIPELINES': settings.ITEM_PIPELINES,
            'DATA_STORE': data_path,
            'CONTENT_FILE': settings.CONTENT_FILE
        })
        process.crawl(
            crawler_or_spidercls=BibleSpider,
            data_store=process.settings.get('DATA_STORE'),
            content_file=process.settings.get('CONTENT_FILE')
        )
        process.start()


class AudioBible(object):
    def __init__(self, operation):
        function = operation[0] if operation[0] in ['init', 'load', 'hear', 'read', 'list', 'find', 'quote', 'help'] else 'help'
        if function in ['hear', 'read']:
            try:
                self.book = operation[1]
            except IndexError:
                self.book = 'GENESIS'
            try:
                chapter = operation[2]
                try:
                    self.chapter = int(chapter)
                except ValueError:
                    self.chapter = 1
            except IndexError:
                self.chapter = 1
        else:
            self.query = " ".join(operation[1:]).strip(" ")
        getattr(self, function, self.help)()

    def init(self):
        print 'downloading content from audiobible.com'
        DownloadBible.process()

    def load(self):
        print 'downloading bible from audiobible.com'
        DownloadBible.process()

    def _open(self, filepath):
        import subprocess, os
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))

    def _get_book(self):
        return self.book.upper()

    def _get_chapter(self):
        return self.chapter

    def get_filename(self, ext):
        book = self._get_book()
        chapter = self._get_chapter()
        return os.path.join(data_path, book, '%s_%d.%s' % (book, chapter, ext))

    def hear(self):
        audio = self.get_filename('mp3')
        print 'opening KJV Bible audio', self.book, self.chapter
        if os.path.exists(audio):
            self._open(audio)
        else:
            print 'Unable to find audio file', audio

    def read(self):
        text = self.get_filename('txt')
        print 'opening KJV Bible text', self.book, self.chapter
        if os.path.exists(text):
            self._open(text)
        else:
            print 'Unable to find text file', text

    def find(self):
        for dirname, dirnames, filenames in os.walk(data_path):
            for filename in filenames:
                if '.txt' in filename:
                    file = os.path.join(dirname, filename)
                    for line in open(file).readlines():
                        match = re.search(self.query, line, re.IGNORECASE)
                        if match:
                            print match.string

    def list(self):
        table_of_contents = {
            'old': {
                'names': [],
                'count': []
            },
            'new': {
                'names': [],
                'count': []
            }
        }
        is_old_testament = True
        if os.path.exists(content_path):
            with open(content_path, 'r') as lines:
                for line in lines:
                    book = json.loads(line)
                    if book['name'].upper() in 'MATTHEW' or not is_old_testament:
                        is_old_testament = False
                        table_of_contents['new']['names'].append(book['name'])
                        table_of_contents['new']['count'].append('%d' % book['chapters_count'])
                    else:
                        table_of_contents['old']['names'].append(book['name'])
                        table_of_contents['old']['count'].append('%d' % book['chapters_count'])

        print '{:<30}{:<30}{:<30}{:<30}'.format('Old Testament', '###', 'New Testament', '##')
        print '{:<30}{:<30}{:<30}{:<30}'.format('=============', '===', '=============', '==')
        for a, b, c, d in zip(
                table_of_contents['old']['names'],
                table_of_contents['old']['count'],
                table_of_contents['new']['names'],
                table_of_contents['new']['count']
        ):
            print '{:<30}{:<30}{:<30}{:<30}'.format(a, b, c, d)

    def quote(self, head=None, tail=None):
        print 'MK 4:23 If any man have ears to hear, let him hear.'

    def help(self):
        parser.print_help()


def parse_args():
    return parser.parse_args()


def main(*args, **kwargs):
    def use_params(
        operation=None,
    ):
        return AudioBible(operation=operation)

    # argparse arguments
    if len(args) > 0 \
            and isinstance(args[0], argparse.Namespace):
        args = args[0]

        return use_params(
            operation=args.operation,
        )
    # dict arguments
    if isinstance(kwargs, dict):
        return use_params(
            operation=kwargs.get('operation'),
        )


def use_parse_args():
    args = parse_args()
    main(args)


def use_keyword_args(**kwargs):
    return main(**kwargs)


if __name__ == '__main__':
    use_parse_args()
