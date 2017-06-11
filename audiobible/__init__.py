#! /usr/bin/env python2

import re
import os
import sys
import json
import argparse
from scrapy.crawler import CrawlerProcess
from kjv.spiders.bible import BibleSpider
from kjv import settings

__version__ = open(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'VERSION')).read().strip()

parser = argparse.ArgumentParser(
    prog='audiobible' or sys.argv[0],
    usage='%(prog)s operation [BOOK] [CHAPTER]',
    description='%(prog)s - King James Version Audio Bible')

parser.add_argument('operation', nargs='+', type=str, help="init, load, hear, read, find, list, quote, help")
parser.add_argument("-b", "--book",  type=str, help="Book to hear, read, find or quote", default=None)
parser.add_argument("-c", "--chapter", type=str, help="Chapter to hear, read, find or quote", default=None)
parser.add_argument("-C", "--context",  type=int, help="Print num lines of leading and trailing context surrounding each match.", default=None)
parser.add_argument("-B", "--before-context", type=int, help="Print num lines of trailing context before each match.", default=None)
parser.add_argument("-A", "--after-context",  type=int, help="Print num lines of trailing context after each match.", default=None)

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

bot_name = settings.BOT_NAME
data_path = os.path.join(os.path.expanduser('~'), settings.DATA_STORE)
content_path = os.path.join(data_path, settings.CONTENT_FILE)
DEFAULT_BOOK = 'GENESIS'
DEFAULT_CHAPTER = 1


class NumberOutOfRangeError(ValueError):
    def __init__(self, *args, **kwargs):
        super(NumberOutOfRangeError, self).__init__(*args, **kwargs)


class BookNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(BookNotFoundError, self).__init__(*args, **kwargs)


class ChapterNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(ChapterNotFoundError, self).__init__(*args, **kwargs)


class DownloadBible(object):
    @staticmethod
    def process():
        process = CrawlerProcess({
            'BOT_NAME': bot_name,
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
    books = []
    book = None
    chapter = None
    context = None
    before_context = None
    after_context = None
    result = None
    query = ''

    def __init__(self, operation, book, chapter, context, before_context, after_context):
        function = operation[0] if operation and operation[0].lower() in [
            'init', 'load', 'hear', 'read', 'list', 'find', 'quote', 'version', 'help'
        ] else 'help'

        if function == 'version':
            print __version__
            sys.exit(0)

        if function in ['hear', 'read', 'list', 'find', 'quote']:
            self._load_books()

        if function not in ['init', 'load', 'list', 'help']:
            self._set(operation, book, chapter)

        if function == 'find':
            self.query = " ".join(operation[1:]).strip(" ")
            self.result = self.find(context, before_context, after_context)
        else:
            self.result = getattr(self, function, self.help)()

    def _set(self, operation, book, chapter):
        if operation[0] not in ['find']:
            try:
                self.book = self._valid('book', operation[1])
            except (IndexError, BookNotFoundError):
                self._valid_book(operation, book)

            try:
                self.chapter = self._valid('chapter', operation[2])
            except (IndexError, ValueError, TypeError, ChapterNotFoundError):
                self._valid_chapter(operation, chapter)
        else:
            if book:
                self._valid_book(operation, book)
            if chapter:
                self._valid_chapter(operation, chapter)

    def _valid_book(self, operation, value):
        try:
            self.book = self._valid('book', value)
        except BookNotFoundError as e:
            try:
                the_book = value if value else operation[1]
                sys.exit('%s: %s' % (e.message, the_book))
            except IndexError:
                self.book = DEFAULT_BOOK

    def _valid_chapter(self, operation, chapter):
        try:
            if len(operation) < 3:
                try:
                    self.chapter = self._valid('chapter', chapter)
                except (ValueError, TypeError, ChapterNotFoundError) as e:
                    the_chapter = chapter if chapter else operation[2]
                    print 'Book:', self.get_book()
                    sys.exit('%s: %s' % (e.message, the_chapter))
            else:
                try:
                    raise ChapterNotFoundError('Chapter Not Found')
                except ChapterNotFoundError as e:
                    the_chapter = chapter if chapter else operation[2]
                    print 'Book:', self.get_book()
                    sys.exit('%s: %s' % (e.message, the_chapter))
        except IndexError:
            self.chapter = DEFAULT_CHAPTER

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

    def get_book(self):
        if self.book:
            return self.book.upper().replace(' ', '_')

    def get_chapter(self):
        return self.chapter

    def get_filename(self, ext):
        book = self.get_book()
        chapter = self.get_chapter()
        return os.path.join(data_path, book, '%s_%s.%s' % (book, chapter, ext))

    def hear(self):
        audio = self.get_filename('mp3')
        print 'opening KJV Bible audio', self.get_book(), self.get_chapter()
        if os.path.exists(audio):
            self._open(audio)
        else:
            print 'Unable to find audio file', audio

    def read(self):
        text = self.get_filename('txt')
        print 'opening KJV Bible text', self.get_book(), self.get_chapter()
        if os.path.exists(text):
            self._open(text)
        else:
            print 'Unable to find text file', text

    def _files(self, path):
        result = []
        for book in self.books:
            book_path = os.path.join(data_path, book['name'].replace(' ', '_'))
            if path in book_path and os.path.isdir(book_path):
                for dirname, dirnames, filenames in os.walk(book_path):
                    numbers = [int(filter(str.isdigit, str(f))) for f in filenames if '.txt' in f]
                    numbers.sort()
                    if numbers:
                        digit = int(filter(str.isdigit, str(filenames[0].replace('.mp3', '.txt'))))
                        for num in numbers:
                            filename = filenames[0].replace('.mp3', '.txt').replace(str(digit), str(num))
                            result.append(os.path.join(dirname, filename))
        return result

    def find(self, context, before, after):
        the_path = data_path
        if self.get_book():
            the_path = os.path.join(the_path, self.get_book())
        if self.get_chapter() is not None:
            the_path = self.get_filename('txt')

        output = []

        def _handle(matched, lines, line):
            if matched:
                if before:
                    for num in range(int(before), 0, -1):
                        verse = lines[line - num]
                        if verse not in output:
                            output.append(verse)

                verse = matched.string
                if verse not in output:
                    output.append(verse)

                if after:
                    for num in range(1, int(after) + 1):
                        verse = lines[line + num]
                        if verse not in output:
                            output.append(verse)

        if context is not None:
            if before is None:
                before = context
            if after is None:
                after = context

        if os.path.isdir(the_path):
            for filename in self._files(the_path):
                lines = []
                for l in open(filename).readlines():
                    lines.append(l)

                for line in range(len(lines)):
                    match = re.search(self.query, lines[line], re.IGNORECASE)
                    _handle(match, lines, line)
        else:
            lines = []
            for l in open(the_path).readlines():
                lines.append(l)

            for line in range(len(lines)):
                match = re.search(self.query, lines[line], re.IGNORECASE)
                _handle(match, lines, line)

        return str("\r\n".join([o for o in output if o])).strip()

    def _load_books(self):
        if os.path.exists(content_path):
            with open(content_path, 'r') as lines:
                for line in lines:
                    self.books.append(json.loads(line))
        return self.books

    def _valid(self, name, value):
        if name is 'book':
            if str(value).upper().replace(' ', '_') in [b['name'].upper().replace(' ', '_') for b in self.books]:
                return str(value).upper().replace(' ', '_')
            else:
                raise BookNotFoundError('Book Not Found')
        if name is 'chapter':
            try:
                if int(value) in [range(1, b['chapters_count'] + 1)
                             for b in self.books if b['name'].upper().replace(' ', '_') == self.get_book()][0]:
                    return value
                else:
                    raise ChapterNotFoundError('Chapter Not Found')
            except (IndexError, TypeError, ValueError) as e:
                raise ChapterNotFoundError('Chapter Not Found')

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
        old = []
        new = []
        output = ''
        for book in self.books:
            if book['name'].upper() in 'MATTHEW' or not is_old_testament:
                is_old_testament = False
                table_of_contents['new']['names'].append(book['name'].replace(' ', '_'))
                table_of_contents['new']['count'].append('%d' % book['chapters_count'])
            else:
                table_of_contents['old']['names'].append(book['name'].replace(' ', '_'))
                table_of_contents['old']['count'].append('%d' % book['chapters_count'])

        for a, z in zip(
                table_of_contents['old']['names'],
                table_of_contents['old']['count'],
        ):
            old.append((a, z))

        for a, z in zip(
                table_of_contents['new']['names'],
                table_of_contents['new']['count'],
        ):
            new.append((a, z))

        for i in range(len(old)):
            try:
                output += '{:<30}|   {:<6}| {:<30}|   {:<4}\r\n'.format(old[i][0], old[i][1], new[i][0], new[i][1])
            except IndexError:
                output += '{:<30}|   {:<6}|\r\n'.format(old[i][0], old[i][1])
        output = '%s\r\n%s' % ('{:<30}|{:<7}|{:<30}|{:<4}\r\n'.format(
            '------------------------------', '---------', '-------------------------------', '--------'), output)
        output = '%s\r\n%s' % (
            '{:<30}|   {:<6}| {:<30}|   {:<4}'.format('Old Testament', '###', 'New Testament', '##'), output)

        return output

    def quote(self, head=None, tail=None):
        return 'MK 4:23 If any man have ears to hear, let him hear.'

    def help(self):
        print """AudioBible %s
==========

    audiobible init                                             # download data about all books and chapters in the KJV
    audiobible load                                             # download all books' and chapters' text and audio mp3 files

    audiobible list                                             # to list all books and the number of chapters each book has

    audiobible hear                                             # to hear the book of "Genesis" chapter 1
    audiobible hear mark                                        # to hear the book of "Mark" chapter 1
    audiobible hear -b mark                                     # to hear the book of "Mark" chapter 1
    audiobible hear mark 4                                      # to hear the book of "Mark" chapter 4
    audiobible hear -b mark -c 4                                # to hear the book of "Mark" chapter 4
    audiobible hear 1_john 3                                    # to hear the book of "1 John" chapter 3
    audiobible hear -b 1_john -c 3                              # to hear the book of "1 John" chapter 3

    audiobible read mark 4                                      # to read Mark 4, (use params like with hear operation)

    audiobible find                                             # to output the whole Bible
    audiobible find -b 2_john                                   # to output the whole book of "2 John"
    audiobible find -b james -c 5                               # to output chapter 5 for the book of "James"
    audiobible find water of life                               # to find water of life, say words to search for as params
    audiobible find water                                       # to find water, say the word to search the whole bible
    audiobible find 'circle of the earth'                       # to find circle of the earth, say the words to search of as a string
    audiobible find circle                                      # or find the same results with just looking for circle

    audiobible find jesus -b luke -c 3 -C 2                     # to find jesus in the book of "Luke" chapter 3, showing 2 verses before and after the matched verse context
    audiobible find circle -A 5 -B 2                            # to show 2 verse before and 5 verses after the matched verse context

==========
        """ % __version__
        parser.print_help()

    def output(self):
        return self.result


def parse_args():
    return parser.parse_args()


def main(*args, **kwargs):
    def use_params(
        operation=None,
        book=None,
        chapter=None,
        context=None,
        before_context=None,
        after_context=None
    ):
        return AudioBible(
            operation=operation,
            book=book,
            chapter=chapter,
            context=context,
            before_context=before_context,
            after_context=after_context
        ).output()

    # argparse arguments
    if len(args) > 0 \
            and isinstance(args[0], argparse.Namespace):
        args = args[0]

        return use_params(
            operation=args.operation,
            book=args.book,
            chapter=args.chapter,
            context=args.context,
            before_context=args.before_context,
            after_context=args.after_context
        )
    # dict arguments
    if isinstance(kwargs, dict):
        return use_params(
            operation=kwargs.get('operation'),
            book=kwargs.get('book'),
            chapter=kwargs.get('chapter'),
            context=kwargs.get('context'),
            before_context=kwargs.get('before_context'),
            after_context=kwargs.get('after_context')
        )


def use_parse_args():
    args = parse_args()
    return main(args)


# for usage from code
def use_keyword_args(**kwargs):
    return main(**kwargs)


if __name__ == '__main__':
    result = use_parse_args()
    if result:
        print result
