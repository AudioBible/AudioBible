#! /usr/bin/env python2

import re
import os
import sys
import json
import random
import argparse
from scrapy.crawler import CrawlerProcess

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from kjv.spiders.bible import BibleSpider
from kjv import settings

__version__ = '0.2.1'


def extended_help():
    return """

https://github.com/AudioBible/AudioBible                    https://github.com/AudioBible/KJV

pip install --upgrade audiobible                            # update AudioBible to the latest version

audiobible update                                           # update AudioBible using pip command internally

audiobible -h | --help                                      # show help
audiobible help                                             # show help

audiobible version                                          # show version number and exit

audiobible init                                             # download data about all books and chapters in the KJV

audiobible load                                             # download all books' and chapters' text and audio mp3 files

audiobible list                                             # to list all books and the number of chapters each book has

audiobible praise                                           # open a browser to a youtube playlist with hymns for praising God

audiobible path daniel                                      # show the path on the hard drive to the book of "Daniel"

audiobible quote                                            # to output a quote

audiobible hear mark                                        # to hear the book of "Mark" chapter 1
audiobible hear mark all                                    # to hear all chapters from the book of "Mark"
audiobible hear -b mark                                     # to hear the book of "Mark" chapter 1
audiobible hear mark 4                                      # to hear the book of "Mark" chapter 4
audiobible hear -b mark -c 4                                # to hear the book of "Mark" chapter 4
audiobible hear 1_john 3                                    # to hear the book of "1 John" chapter 3
audiobible hear -b 1_john -c 3                              # to hear the book of "1 John" chapter 3
audiobible hear -b mark -c all                              # same as hear mark all, there is a bug i can't fix where it starts to play from the last file,
                                                            #   just double click on the first one and it will start from the beginning playing the rest

audiobible read mark 4                                      # to read Mark 4, (use params like with hear operation)

audiobible show mark 4                                      # to show the book of "Mark" chapter 4 text in the terminal, specify params like with hear operation

audiobible find                                             # to output the whole Bible
audiobible find -b 2_john                                   # to output the whole book of "2 John"
audiobible find -b james -c 5                               # to output chapter 5 for the book of "James"
audiobible find water of life                               # to find water of life, say words to search for as params
audiobible find water                                       # to find water, say the word to search the whole bible
audiobible find 'it is done'                                # to find it is done, say the words to search as a string
audiobible find circle of the earth                         # to find circle of the earth

audiobible find jesus -b luke -c 3 -C 2                     # to find jesus in the book of "Luke" chapter 3, showing 2 verses before and after the matched verse context
audiobible find circle -A 5 -B 2                            # to show 2 verse before and 5 verses after the matched verse context

audiobible quote                                            # usage is same as with find operation


# THE EARTH IS FLAT! [RESEARCH IT ON YOUTUBE](https://www.youtube.com/results?search_query=flat+earth&page=&utm_source=opensearch)!

# THIS IS POSITIVE INFO! IT'S A MATTER OF PERSPECTIVE!

# THE WAR ON TERROR IS A WAR ON YOU!

## God is so kind that it is impossible to imagine His unbounded kindness

"""

parser = argparse.ArgumentParser(
    prog='audiobible' or sys.argv[0],
    usage=extended_help() + """audiobible [-h] [-b BOOK] [-c CHAPTER] [-C CONTEXT] [-B BEFORE_CONTEXT] [-A AFTER_CONTEXT] operation [words ...]""",
    description='%(prog)s '+__version__+' - King James Version Audio Bible')

parser.add_argument('operation', nargs='+', type=str, help="init, load, hear, read, find, show, list, quote, praise, path, version, help, update")
parser.add_argument("-b", "--book", type=str, help="book to hear, read, find or quote", default=None)
parser.add_argument("-c", "--chapter", type=str, help="chapter to hear, read, find or quote", default=None)
parser.add_argument("-C", "--context", type=int, help="print num lines of leading and trailing context surrounding each match.", default=None)
parser.add_argument("-B", "--before-context", type=int, help="print num lines of trailing context before each match.", default=None)
parser.add_argument("-A", "--after-context", type=int, help="print num lines of trailing context after each match.", default=None)

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

bot_name = settings.BOT_NAME

base_path = os.environ.get('BOOKS_PATH', None)
if not base_path:
    base_path = os.path.expanduser('~')

data_path = os.path.join(os.path.abspath(base_path), settings.DATA_STORE)
content_path = os.path.join(data_path, settings.CONTENT_FILE)
DEFAULT_BOOK = None
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


class FileNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(FileNotFoundError, self).__init__(*args, **kwargs)


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
        function = operation[0] if operation[0].lower() in [
            'init', 'load', 'hear', 'read', 'list', 'show', 'find', 'quote',
            'path', 'praise', 'version', 'help', 'update', 'upgrade',
        ] else 'help'

        if 'v' in function:
            print(__version__)
            sys.exit(0)

        if 'update' in function:
            self.update()
            sys.exit(0)

        proceed = True
        if function not in ['init', 'load', 'help', 'praise']:
            self._load_books()
            self._set(operation, book, chapter)
            if not self.book:
                self.result = self.list()
                proceed = False

        if function in ['find', 'quote']:
            self.query = " ".join(operation[1:]).strip(" ")
            self.result = getattr(self, function)(context, before_context, after_context)
        else:
            if proceed:
                self.result = getattr(self, function, self.help)()

    def _load_books(self):
        if os.path.exists(content_path):
            with open(content_path, 'r') as lines:
                for line in lines:
                    self.books.append(json.loads(line))
        return self.books

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
                    print('Book:', self.get_book())
                    sys.exit('%s: %s' % (e.message, the_chapter))
            else:
                try:
                    raise ChapterNotFoundError('Chapter Not Found')
                except ChapterNotFoundError as e:
                    the_chapter = chapter if chapter else operation[2]
                    print('Book:', self.get_book())
                    sys.exit('%s: %s' % (e.message, the_chapter))
        except IndexError:
            self.chapter = DEFAULT_CHAPTER

    def _valid(self, name, value):
        if name is 'book':
            if str(value).upper().replace(' ', '_') in [b['name'].upper().replace(' ', '_') for b in self.books]:
                return str(value).upper().replace(' ', '_')
            else:
                raise BookNotFoundError('Book Not Found')
        if name is 'chapter':
            try:
                if value != 'all':
                    if int(value) in [range(1, b['chapters_count'] + 1)
                                      for b in self.books if b['name'].upper().replace(' ', '_') == self.get_book()][0]:
                        return value
                    else:
                        raise ChapterNotFoundError('Chapter Not Found')
                else:
                    val = [range(1, b['chapters_count'] + 1)
                           for b in self.books if b['name'].upper().replace(' ', '_') == self.get_book()][0]
                    return val
            except (IndexError, TypeError, ValueError) as e:
                raise ChapterNotFoundError('Chapter Not Found')

    def init(self):
        print('downloading content from audiobible.com')
        DownloadBible.process()
        return self

    def load(self):
        print('downloading bible from audiobible.com')
        DownloadBible.process()
        return self

    def _open(self, filepath):
        import subprocess, os
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))
        return self

    def get_book(self):
        if self.book:
            return self.book.upper().replace(' ', '_')

    def get_chapter(self):
        return self.chapter

    def get_filenames(self, ext):
        book = self.get_book()
        chapter = self.get_chapter()
        paths = []
        if isinstance(chapter, list):
            for c in chapter:
                paths.append(os.path.join(data_path, book, '%s_%s.%s' % (book, c, ext)))
        else:
            paths.append(os.path.join(data_path, book, '%s_%s.%s' % (book, chapter, ext)))
        return paths

    def praise(self):
        self._open("https://www.youtube.com/results?search_query=praise+worship+hymns")

    def update(self):
        import subprocess
        subprocess.call(('pip', 'install', '--upgrade', 'audiobible'))
        return self

    def path(self):
        return os.path.join(data_path, self.get_book())

    def hear(self):
        audio = self.get_filenames('mp3')
        for a in audio:
            if os.path.exists(a):
                self._open(a)

    def read(self):
        text = self.get_filenames('txt')
        for t in text:
            if os.path.exists(t):
                self._open(t)

    def show(self):
        text = self.get_filenames('txt')
        texts = []
        for t in text:
            if os.path.exists(t):
                texts.append(open(t).read().strip())
        return "\r\n".join(texts).strip()

    def _files(self, path):
        out = []
        for book in self.books:
            book_path = os.path.join(data_path, book['name'].replace(' ', '_'))
            if path in book_path and os.path.isdir(book_path):
                for dirname, dirnames, filenames in os.walk(book_path):
                    try:
                        numbers = [int(filter(str.isdigit, str(f))) for f in filenames if '.txt' in f]
                    except:
                        numbers = [int("".join(list(filter(str.isdigit, str(f))))) for f in filenames if '.txt' in f]

                    numbers.sort()
                    if numbers:
                        digit = int("".join(list(filter(str.isdigit, str(filenames[0].replace('.mp3', '.txt'))))))
                        for num in numbers:
                            filename = filenames[0].replace('.mp3', '.txt').replace(str(digit), str(num))
                            out.append(os.path.join(dirname, filename))
        return out

    def get_lines(self, the_path, callback):
        lines = []

        def _get_lines(path):
            if os.path.isdir(path):
                for filename in self._files(path):
                    if '.txt' in filename and os.path.exists(filename):
                        for l in open(filename).readlines():
                            lines.append(l)
            else:
                if '.txt' in path and os.path.exists(path):
                    for l in open(path).readlines():
                        lines.append(l)

        if isinstance(the_path, list):
            for p in the_path:
                _get_lines(p)
        else:
            _get_lines(the_path)

        callback(lines)

    def _get_text(self, type, context, before, after):
        the_path = data_path
        if self.get_book():
            the_path = os.path.join(the_path, self.get_book())
            if self.get_chapter() is not None:
                the_path = self.get_filenames('txt')

        output = []

        if context is not None:
            if before is None:
                before = context
            if after is None:
                after = context

        if type == 'find':
            def _process(lines):
                for line in range(len(lines)):
                    match = re.search(self.query, lines[line], re.IGNORECASE)
                    if match:
                        if before:
                            for num in range(int(before), 0, -1):
                                verse = lines[line - num]
                                if verse not in output:
                                    output.append(verse)

                        verse = match.string
                        if verse not in output:
                            output.append(verse)

                        if after:
                            for num in range(1, int(after) + 1):
                                verse = lines[line + num]
                                if verse not in output:
                                    output.append(verse)

            self.get_lines(the_path, _process)
        elif type == 'quote':
            def _process(lines):
                idx = random.choice(range(len(lines)))
                if before:
                    for num in range(int(before), 0, -1):
                        verse = lines[idx - num]
                        if verse not in output:
                            output.append(verse)

                verse = lines[idx]
                if verse not in output:
                    output.append(verse)

                if after:
                    for num in range(1, int(after) + 1):
                        verse = lines[idx + num]
                        if verse not in output:
                            output.append(verse)

            self.get_lines(the_path, _process)

        return str("\r\n".join([o for o in output if o])).strip()

    def find(self, context, before, after):
        return self._get_text('find', context, before, after)

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

    def quote(self, context=None, before=None, after=None):
        return self._get_text('quote', context, before, after)

    def help(self):
        parser.print_help()
        return self

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
        print(result)
