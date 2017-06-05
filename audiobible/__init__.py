#! /usr/bin/env python2

import os
import sys
import json
import argparse
from scrapy.crawler import CrawlerProcess
from kjv.spiders.bible import BibleSpider
from kjv import settings

parser = argparse.ArgumentParser(
    prog='audiobible' or sys.argv[0],
    description='%(prog)s - King James Version Audio Bible')

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
    def __init__(self, operation, book=None, chapter=None):
        self.book = book
        self.chapter = chapter
        getattr(self, operation, self.help)()

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

    def hear(self):
        print 'playing audio', self.book, self.chapter
        # self._open('')

    def read(self):
        print 'opening bible text', self.book, self.chapter
        # self._open('')

    def list(self):
        table_of_contents = {
            'old': [],
            'new': []
        }
        is_old_testament = True
        if os.path.exists(content_path):
            with open(content_path, 'r') as lines:
                for line in lines:
                    book = json.loads(line)
                    if book['name'].upper() in 'MATTHEW' or not is_old_testament:
                        is_old_testament = False
                        table_of_contents['new'].append(book['name'])
                    else:
                        table_of_contents['old'].append(book['name'])

        print '{:<30}{:<30}'.format('Old Testament', 'New Testament')
        print '{:<30}{:<30}'.format('=============', '=============')
        for a, b in zip(table_of_contents['old'], table_of_contents['new']):
            print '{:<30}{:<30}'.format(a, b)

    def quote(self, head=None, tail=None):
        print 'MK 4:23 If any man have ears to hear, let him hear.'

    def help(self):
        parser.print_help()


def parse_args():
    parser.add_argument('operation', choices=['init', 'load', 'hear', 'read', 'list', 'quote', 'help'])
    parser.add_argument("-b", "--book",  type=str, help="Book to hear, read or quote", default='Mark')
    parser.add_argument("-c", "--chapter", type=str, help="Chapter to hear, read or quote", default="1")

    return parser.parse_args()


def main(*args, **kwargs):
    def use_params(
        operation=None,
        book=None,
        chapter=None,
    ):
        return AudioBible(operation=operation, book=book, chapter=chapter)

    # argparse arguments
    if len(args) > 0 \
            and isinstance(args[0], argparse.Namespace):
        args = args[0]

        return use_params(
            operation=args.operation,
            book=args.book,
            chapter=args.chapter
        )
    # dict arguments
    if isinstance(kwargs, dict):
        return use_params(
            operation=kwargs.get('operation'),
            book=kwargs.get('book'),
            chapter=kwargs.get('chapter')
        )


def use_parse_args():
    args = parse_args()
    return main(args)


def use_keyword_args(**kwargs):
    return main(**kwargs)


if __name__ == '__main__':
    use_parse_args()
