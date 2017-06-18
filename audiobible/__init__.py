#! /usr/bin/env python2

try:
    import re
    import os
    import sys
    import json
    import random
    import string
    import argparse
    from scrapy.crawler import CrawlerProcess

    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    from kjv.bible.bible import BibleSpider
    from kjv.speakers.speakers import SpeakersSpider
    from kjv.topics.topics import TopicsSpider

    from kjv import settings

    __version__ = '0.7.1'


    def extended_help():
        return """

https://github.com/AudioBible/AudioBible                    https://github.com/AudioBible/KJV

pip install --upgrade audiobible                            # update AudioBible to the latest version

audiobible update                                           # update AudioBible using pip command internally

audiobible -h | --help                                      # show help
audiobible help                                             # show help

audiobible version                                          # show version number and exit

audiobible init                                             # download data about all books and chapters in the KJV
audiobible init speaker                                     # download all the names of speakers from sermonaudio.com
audiobible init topics                                      # download all the topics from sermonaudio.com

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
audiobible find circle of the earth -a partial              # to find query using fuzzy partial algorithm, also try: 'ratio', 'set', 'sort'; default is 'regex'
                                                            # algorithms are only for the find operation

audiobible find jesus -b luke -c 3 -C 2                     # to find jesus in the book of "Luke" chapter 3, showing 2 verses before and after the matched verse context
audiobible find circle -A 5 -B 2                            # to show 2 verse before and 5 verses after the matched verse context

audiobible quote                                            # usage is same as with find operation

audiobible sermons                                          # opens the default browser to http://sermonaudio.com
                                                            #  usage is same as with hear operation
audiobible sermons -b mark -s "Charles Lawson"              # open browser to sermon "Charles Lawson" preaching the book of "Mark"

# THE EARTH IS FLAT! [RESEARCH IT ON YOUTUBE](https://www.youtube.com/results?search_query=flat+earth&page=&utm_source=opensearch)!

# THIS IS POSITIVE INFO! IT'S A MATTER OF PERSPECTIVE!

# THE WAR ON TERROR IS A WAR ON YOU!

## God is so kind that it is impossible to imagine His unbounded kindness

"""

    parser = argparse.ArgumentParser(
        prog='audiobible' or sys.argv[0],
        usage=extended_help() + """audiobible [-h] [-b BOOK] [-c CHAPTER] [-C CONTEXT] [-B BEFORE_CONTEXT] [-A AFTER_CONTEXT] operation [words ...]""",
        description='%(prog)s '+__version__+' - King James Version Audio Bible')

    parser.add_argument('operation', nargs='+', type=str, help="init, load, hear, read, find, show, list, quote, praise, sermons, path, version, help, update")
    parser.add_argument("-a", "--algorithm", choices=['regex', 'ratio', 'partial', 'sort', 'set'])
    parser.add_argument("-b", "--book", type=str, help="book to hear, read, find or quote", default=None)
    parser.add_argument("-c", "--chapter", type=str, help="chapter to hear, read, find or quote", default=None)
    parser.add_argument("-C", "--context", type=int, help="print num lines of leading and trailing context surrounding each match.", default=None)
    parser.add_argument("-B", "--before-context", type=int, help="print num lines of trailing context before each match.", default=None)
    parser.add_argument("-A", "--after-context", type=int, help="print num lines of trailing context after each match.", default=None)
    parser.add_argument("-s", "--speaker", type=str, help="speaker to hear a sermon from", default=None)
    parser.add_argument("-t", "--topic", type=str, help="topic to hear a sermon on", default=None)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    bot_name = settings.BOT_NAME

    base_path = os.environ.get('BOOKS_PATH', None)
    if not base_path:
        base_path = os.path.expanduser('~')

    data_path = os.path.join(os.path.abspath(base_path), settings.DATA_STORE)
    content_path = os.path.join(data_path, settings.CONTENT_FILE)
    speakers_path = os.path.join(data_path, settings.SPEAKERS_FILE)
    topics_path = os.path.join(data_path, settings.TOPICS_FILE)
    DEFAULT_BOOK = None
    DEFAULT_CHAPTER = 1
    DEFAULT_ALGORITHM = 'regex'

except (KeyboardInterrupt, SystemExit):
    sys.exit(0)


class NumberOutOfRangeError(ValueError):
    def __init__(self, *args, **kwargs):
        super(NumberOutOfRangeError, self).__init__(*args, **kwargs)


class BookNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(BookNotFoundError, self).__init__(*args, **kwargs)


class ChapterNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(ChapterNotFoundError, self).__init__(*args, **kwargs)


class SpeakerNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(SpeakerNotFoundError, self).__init__(*args, **kwargs)


class TopicNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(TopicNotFoundError, self).__init__(*args, **kwargs)


class FileNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(FileNotFoundError, self).__init__(*args, **kwargs)


class PathNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(PathNotFoundError, self).__init__(*args, **kwargs)


class DataNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super(DataNotFoundError, self).__init__(*args, **kwargs)


class Download(object):
    @staticmethod
    def _bible():
        pipelines = {
            bot_name + '.pipelines.KjvPipeline': 1,
            bot_name + '.pipelines.Mp3Pipeline': 2,
        }
        spider_module = 'kjv.bible'
        process = CrawlerProcess({
            'BOT_NAME': bot_name,
            'SPIDER_MODULES': settings.SPIDER_MODULES,
            'NEWSPIDER_MODULE': spider_module,
            'USER_AGENT': settings.USER_AGENT,
            'ROBOTSTXT_OBEY': settings.ROBOTSTXT_OBEY,
            'ITEM_PIPELINES': pipelines,
            'DATA_STORE': data_path,
            'CONTENT_FILE': settings.CONTENT_FILE
        })
        process.crawl(
            crawler_or_spidercls=BibleSpider,
            data_store=process.settings.get('DATA_STORE'),
            content_file=process.settings.get('CONTENT_FILE')
        )
        process.start()

    @staticmethod
    def init():
        Download._bible()

    @staticmethod
    def load():
        if os.path.exists(content_path):
            Download._bible()
        else:
            sys.stdout.write('No books found. Please run this command to download them:\r\naudiobible init\r\n')
    @staticmethod
    def speakers():
        pipelines = {
            bot_name + '.pipelines.SpeakerPipeline': 1,
        }
        spider_module = 'kjv.speakers'
        process = CrawlerProcess({
            'BOT_NAME': bot_name,
            'SPIDER_MODULES': settings.SPIDER_MODULES,
            'NEWSPIDER_MODULE': spider_module,
            'USER_AGENT': settings.USER_AGENT,
            'ROBOTSTXT_OBEY': settings.ROBOTSTXT_OBEY,
            'ITEM_PIPELINES': pipelines,
            'DATA_STORE': data_path,
            'SPEAKERS_FILE': settings.SPEAKERS_FILE
        })
        process.crawl(
            crawler_or_spidercls=SpeakersSpider,
        )
        process.start()

    @staticmethod
    def topics():
        pipelines = {
            bot_name + '.pipelines.TopicPipeline': 1,
        }
        spider_module = 'kjv.topics'
        process = CrawlerProcess({
            'BOT_NAME': bot_name,
            'SPIDER_MODULES': settings.SPIDER_MODULES,
            'NEWSPIDER_MODULE': spider_module,
            'USER_AGENT': settings.USER_AGENT,
            'ROBOTSTXT_OBEY': settings.ROBOTSTXT_OBEY,
            'ITEM_PIPELINES': pipelines,
            'DATA_STORE': data_path,
            'TOPICS_FILE': settings.TOPICS_FILE
        })
        process.crawl(
            crawler_or_spidercls=TopicsSpider,
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
    ratio = 'regex'
    scope = None
    speaker = None
    topic = None
    speakers = {}
    topics = {}

    def __init__(self, operation, algorithm, book, chapter, speaker, topic, context, before_context, after_context):
        function = operation[0] if operation[0].lower() in [
            'init', 'load', 'hear', 'read', 'list', 'show', 'find', 'quote',
            'path', 'praise', 'sermon', 'sermons', 'version', 'help', 'update', 'upgrade',
        ] else 'help'

        if 'version' in function:
            sys.stdout.write('%s\r\n' % __version__)
            sys.exit(0)

        if 'update' in function:
            self.update()
            sys.exit(0)

        if 'init' in function or 'list' in function:
            self.scope = operation[1] if len(operation) > 1 else None

        proceed = True
        if function not in ['init', 'load', 'help', 'praise']:
            self._load_books()
            if function in ['sermons', 'list']:
                self._load_speakers()
                self._load_topics()
            # if function not in ['list']:
            self._set(operation, book, chapter, speaker, topic)
            if not self.book and function not in 'sermons':
                self.result = self.list()
                proceed = False

        if function in ['find', 'quote']:
            if algorithm in ['regex', 'ratio', 'partial', 'sort', 'set']:
                self.algorithm = algorithm
            else:
                self.algorithm = DEFAULT_ALGORITHM
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

    def _load_speakers(self):
        self.speakers = dict(zip(list(string.ascii_uppercase), [
            [], [], [], [], [], [], [], [], [], [], [], [], [],
            [], [], [], [], [], [], [], [], [], [], [], [], [],
        ]))
        letters = string.ascii_uppercase
        for l in range(len(letters)):
            path = speakers_path % letters[l]
            if os.path.exists(path):
                with open(path, 'r') as lines:
                    for line in lines:
                        data = json.loads(line)
                        if data['name'][0] == letters[l]:
                            self.speakers[letters[l]].append([data['name'], data['path']])
        return self.speakers

    def _load_topics(self):
        self.topics = dict(zip(list(string.ascii_uppercase), [[]] * len(string.ascii_uppercase)))
        letters = string.ascii_uppercase
        for l in range(len(letters)):
            path = topics_path % letters[l].strip()
            if os.path.exists(path):
                with open(path, 'r') as lines:
                    for line in lines:
                        self.topics[letters[l]].append(json.loads(line))
        return self.topics

    def _set(self, operation, book, chapter, speaker, topic):
        if operation[0] not in ['find', 'sermons', 'list']:
            try:
                self.book = self._valid('book', operation[1])
            except (IndexError, BookNotFoundError):
                self._valid_book(operation, book)

            try:
                self.chapter = self._valid('chapter', operation[2])
            except (IndexError, ValueError, TypeError, ChapterNotFoundError):
                self._valid_chapter(operation, chapter)
        # elif operation[0] in ['list', 'sermon', 'sermons']:
        #     try:
        #         self.speaker = self._valid('speaker', operation[2])
        #     except (IndexError, SpeakerNotFoundError):
        #         self._valid_speaker(operation, speaker)
        #
        #     try:
        #         self.topic = self._valid('topic', operation[3])
        #     except (IndexError, SpeakerNotFoundError):
        #         self._valid_topic(operation, topic)
        else:
            if book:
                self._valid_book(operation, book)
            if chapter:
                self._valid_chapter(operation, chapter)
            if speaker:
                self.speaker = speaker
            elif len(operation) > 2:
                self.speaker = operation[2]
            if topic:
                self.topic = topic
            elif len(operation) > 3:
                self.topic = operation[3]
            # if speaker:
            #     self._valid_speaker(operation, speaker)

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
                    sys.stdout.write('Book: %s\r\n' % self.get_book())
                    sys.exit('%s: %s' % (e.message, the_chapter))
            else:
                try:
                    raise ChapterNotFoundError('Chapter Not Found')
                except ChapterNotFoundError as e:
                    the_chapter = chapter if chapter else operation[2]
                    sys.stdout.write('Book: %s\r\n' % self.get_book())
                    sys.exit('%s: %s' % (e.message, the_chapter))
        except IndexError:
            self.chapter = DEFAULT_CHAPTER

    # def _valid_speaker(self, operation, speaker):
    #     found = False
    #     if speaker:
    #         initial = speaker[0].upper()
    #         print 'init:',initial
    #         for sdx in range(len(self.speakers[initial])):
    #             match = re.search(speaker, self.speakers[initial][sdx][0], re.IGNORECASE)
    #             if match:
    #                 found = match.string
    #                 break
    #
    #         if found:
    #             return found
    #         else:
    #             raise SpeakerNotFoundError('Speaker Not Found')
    #
    # def _valid_topic(self, operation, topic):
    #     found = False
    #     if topic:
    #         initial = topic[0]
    #         for sdx in range(len(self.topics[initial])):
    #             if topic in self.topics[initial][sdx][0]:
    #                 found = True
    #
    #         if found:
    #             self.topic = topic

    def _valid(self, name, value):
        if name is 'book':
            found = None
            for bdx in range(len(self.books)):
                book = str(value).upper().replace(' ', '_')
                match = re.search(book, self.books[bdx]['name'].replace(' ', '_'), re.IGNORECASE)
                if match:
                    found = match.string
                    break

            if found:
                return found
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
        # if name is 'speaker':
        #     found = None
        #     try:
        #         initial = value[0].upper()
        #         if initial in self.speakers.keys():
        #             for bdx in range(len(self.speakers[initial])):
        #                 match = re.search(value, self.speakers[initial][bdx][0], re.IGNORECASE)
        #                 if match:
        #                     found = match.string
        #                     break
        #
        #             if found:
        #                 return value
        #             else:
        #                 raise SpeakerNotFoundError('Speaker Not Found')
        #         else:
        #             raise SpeakerNotFoundError('Speaker Not Found')
        #     except (IndexError, TypeError, ValueError) as e:
        #         raise SpeakerNotFoundError('Speaker Not Found')
        # if name is 'topic':
        #     try:
        #         pass
        #     except (IndexError, TypeError, ValueError) as e:
        #         raise TopicNotFoundError('Topic Not Found')

    def init(self):
        if not self.scope:
            return Download.init()
        elif self.scope in 'bible':
            return Download.load()
        elif self.scope in 'speakers' or self.scope in 'preachers':
            return Download.speakers()
        elif self.scope in 'topics':
            return Download.topics()

    def load(self):
        return Download.load()

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

    def sermons(self):
        if self.speaker:
            speaker = "&subsetCat=speaker&subsetItem=%s" % self.speaker
        else:
            speaker = ''

        if self.get_book():
            if not isinstance(self.get_chapter(), list):
                chapter = self.get_chapter()
            else:
                chapter = ''
            self._open(
                "http://www.sermonaudio.com/search.asp?BibleOnly=true&keyword=%s&chapter=%s%s" %
                (self.get_book(), chapter, speaker))
        elif self.topic:
            self._open(
                "http://www.sermonaudio.com/search.asp?currSection=sermonstopic&keyworddesc=%s&keyword=%s%s" %
                (self.topic, self.topic, speaker)
            )
        else:
            self._open("http://sermonaudio.com")

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
            else:
                return 'File Not Found: %s\r\nPlease run this command to download it:\r\naudiobible load\r\n' % a

    def read(self):
        text = self.get_filenames('txt')
        for t in text:
            if os.path.exists(t):
                self._open(t)
            else:
                return 'File Not Found: %s\r\nPlease run this command to download it:\r\naudiobible load\r\n' % t

    def show(self):
        text = self.get_filenames('txt')
        texts = []
        for t in text:
            if os.path.exists(t):
                for l in open(t).readlines():
                    texts.append('%s\r\n' % l.strip())
            else:
                return 'File Not Found: %s\r\nPlease run this command to download it:\r\naudiobible load\r\n' % t
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
            if os.path.exists(path):
                if os.path.isdir(path):
                    for filename in self._files(path):
                        if '.txt' in filename and os.path.exists(filename):
                            for l in open(filename).readlines():
                                lines.append('%s\r\n' % l.strip())
                else:
                    if '.txt' in path and os.path.exists(path):
                        for l in open(path).readlines():
                            lines.append('%s\r\n' % l.strip())

        if isinstance(the_path, list):
            for p in the_path:
                _get_lines(p)
        else:
            _get_lines(the_path)

        callback(lines)

    def _get_text(self, type, context, before, after):
        if not self.books:
            return 'No books found. Please run these commands to download them:\r\naudiobible init\r\naudiobible load\r\n'
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
                                try:
                                    verse = lines[line - num]
                                    if verse not in output:
                                        output.append(verse)
                                except IndexError:
                                    pass

                        verse = match.string
                        if verse not in output:
                            output.append(verse)

                        if after:
                            for num in range(1, int(after) + 1):
                                try:
                                    verse = lines[line + num]
                                    if verse not in output:
                                        output.append(verse)
                                except IndexError:
                                    pass

            def _fuzz(lines):
                scorer = fuzz.ratio
                if self.algorithm == 'partial':
                    scorer = fuzz.partial_ratio
                elif self.algorithm == 'sort':
                    scorer = fuzz.token_sort_ratio
                elif self.algorithm == 'set':
                    scorer = fuzz.token_set_ratio

                res = process.extract(self.query, lines, scorer=scorer)
                for rdx in range(len(res)):
                    if res[rdx][1] >= 50:
                        verse = res[rdx][0]
                        if verse not in output:
                            output.append(verse)
            try:
                if self.algorithm != 'regex':
                    from fuzzywuzzy import process
                    from fuzzywuzzy import fuzz
                    self.get_lines(the_path, _fuzz)
                else:
                    self.get_lines(the_path, _process)
            except ImportError:
                self.get_lines(the_path, _process)

        elif type == 'quote':
            def _process(lines):
                if lines:
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
                else:
                    raise DataNotFoundError()

            try:
                self.get_lines(the_path, _process)
            except DataNotFoundError as e:
                return "No Data Found. Please run these commands to download:\r\naudiobible init\r\naudiobible load\r\n"

        return str("\r\n".join([o for o in output if o])).strip()

    def find(self, context, before, after):
        return self._get_text('find', context, before, after)

    def list(self):
        output = ''
        if not self.scope or 'books' in self.scope:
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
            if self.books:
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
            else:
                output = "No books found. Please run this command to download them:\r\n"
                output += "audiobible init\r\n"
                # output += "audiobible load\r\n"
        elif 'speakers' in self.scope:
            if len(self.speakers['A']) > 0:
                for k in self.speakers.keys():
                    for s in self.speakers[k]:
                        if self.speaker:
                            match = re.search(
                                self.speaker,
                                s[1].replace('speaker/', '').replace('_', ' '),
                                re.IGNORECASE
                            )
                            if match:
                                output += "%s\r\n" % match.string
                        else:
                            output += "%s\r\n" % s[1].replace('speaker/', '').replace('_', ' ')
            else:
                output = 'No speakers found. Please run this command to download them:\r\n'
                output += 'audiobible init speakers\r\n'
        elif 'topics' in self.scope:
            found = False
            if len(self.topics['A']) > 0:
                for k in self.topics.keys():
                    if not found:
                        for t in self.topics[k]:
                            if self.topic:
                                match = re.search(
                                    self.topic,
                                    t['name'],
                                    re.IGNORECASE
                                )
                                if match:
                                    found = True
                                    output += "%s\r\n" % match.string
                            else:
                                found = True
                                output += "%s\r\n" % t["name"]
            else:
                output = 'No topics found. Please run this command to download them:\r\n'
                output += 'audiobible init topics\r\n'
        return output

    def quote(self, context=None, before=None, after=None):
        return self._get_text('quote', context, before, after)

    def help(self):
        return parser.print_help()

    def output(self):
        return self.result


def parse_args():
    return parser.parse_args()


def main(*args, **kwargs):
    def use_params(
        operation=None,
        algorithm=None,
        book=None,
        chapter=None,
        speaker=None,
        topic=None,
        context=None,
        before_context=None,
        after_context=None
    ):
        try:
            return AudioBible(
                operation=operation,
                algorithm=algorithm,
                book=book,
                chapter=chapter,
                speaker=speaker,
                topic=topic,
                context=context,
                before_context=before_context,
                after_context=after_context
            ).output()
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)

    # argparse arguments
    if len(args) > 0 \
            and isinstance(args[0], argparse.Namespace):
        args = args[0]

        return use_params(
            operation=args.operation,
            algorithm=args.algorithm,
            book=args.book,
            chapter=args.chapter,
            speaker=args.speaker,
            topic=args.topic,
            context=args.context,
            before_context=args.before_context,
            after_context=args.after_context
        )
    # dict arguments
    if isinstance(kwargs, dict):
        return use_params(
            operation=kwargs.get('operation'),
            algorithm=kwargs.get('algorithm'),
            book=kwargs.get('book'),
            chapter=kwargs.get('chapter'),
            speaker=kwargs.get('speaker'),
            topic=kwargs.get('topic'),
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
        sys.stdout.write("%s\r\n" % str(result.encode('utf-8')).strip())
