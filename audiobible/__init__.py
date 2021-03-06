#! /usr/bin/env python2

__version__ = '0.7.9'

try:
    import re
    import os
    import sys
    import json
    import string
    import argparse

    def extended_help():
        return """

https://github.com/AudioBible/AudioBible                    https://github.com/AudioBible/KJV

pip install --upgrade audiobible                            # update AudioBible to the latest version

audiobible update                                           # update AudioBible using pip command internally

audiobible -h | --help                                      # show help
audiobible help                                             # show help

audiobible version                                          # show version number and exit

audiobible init git                                         # git clone all books and data from git repo instead of using spiders in steps
audiobible init                                             # download data about all books and chapters in the KJV, step 1
audiobible init bible                                       # download all books and mp3 audiofiles, step 2
audiobible init speaker                                     # download all the names of speakers from sermonaudio.com, step 3
audiobible init topics                                      # download all the topics from sermonaudio.com, step 4
audiobible init words                                       # download all the words from kingjamesbibledictionary.com, step 5

audiobible dict                                             # open browser to http://www.kingjamesbibledictionary.com
audiobible dict Amen                                        # open browser to "Amen" in the online dictionary
audiobible dict H2                                          # open browser to Strong's number definition online

audiobible hub mark 4                                       # open browser to interlinear biblehub.com book of "Mark" 

audiobible list                                             # to list all books and the number of chapters each book has
audiobible list speakers                                    # to list all speakers found on sermonaudio.com
audiobible list speakers this                               # to list all speakers which have this in there name
audiobible list topics                                      # to list all topics found on sermonaudio.com
audiobible list words                                       # to list all words found on kingjamesbibledictionary.com
audiobible list words this                                  # to list all words and strong's numbers, which have "this" in the word
audiobible list words H2                                    # to list all words which are associated with the strong's number "H2"

audiobible words this                                       # show definition/s and other data for the word "this"
audiobible words H2                                         # show definition/s and other data for the strong's number "H2"

audiobible praise                                           # open a browser to a youtube playlist with hymns for praising God

audiobible path daniel                                      # show the path on the hard drive to the book of "Daniel"

audiobible sermons                                          # opens the default browser to http://sermonaudio.com
audiobible sermons -b mark -s "Charles Lawson"              # open browser to sermon "Charles Lawson" preaching the book of "Mark"

audiobible quote                                            # to output a quote
audiobible quote -A2 -B1                                    # to output a quote having four verses, two after and one before the random selected quote

audiobible hear mark                                        # to hear the book of "Mark" chapter 1
audiobible hear mark all                                    # to hear all chapters from the book of "Mark"
audiobible hear -b mark                                     # to hear the book of "Mark" chapter 1
audiobible hear mark 4                                      # to hear the book of "Mark" chapter 4
audiobible hear -b mark -c 4                                # to hear the book of "Mark" chapter 4
audiobible hear 1_john 3                                    # to hear the book of "1 John" chapter 3
audiobible hear -b 1_john -c 3                              # to hear the book of "1 John" chapter 3
audiobible hear -b mark -c all                              # same as hear mark all

audiobible read mark 4                                      # to read Mark 4, (use params like with hear operation)

audiobible show mark 4                                      # to show the book of "Mark" chapter 4 text in the terminal, specify params like with hear operation

audiobible find                                             # to output the whole Bible
audiobible find REV 22:17                                   # to output a specific verse
audiobible find -b 2_john                                   # to output the whole book of "2 John"
audiobible find -b james -c 5                               # to output chapter 5 for the book of "James"
audiobible find water of life                               # to find water of life, say words to search for as params
audiobible find water                                       # to find water, say the word to search the whole bible
audiobible find 'it is done'                                # to find it is done, say the words to search as a string
audiobible find circle of the earth -a partial              # to find query using fuzzy partial algorithm, also try: 'ratio', 'set', 'sort'; default is 'regex'
                                                            # algorithms are only for the find operation

audiobible find jesus -b luke -c 3 -C 2                     # to find jesus in the book of "Luke" chapter 3, showing 2 verses before and after the matched verse context
audiobible find circle -A 5 -B 2                            # to show 2 verse before and 5 verses after the matched verse context


# THE EARTH IS FLAT! [RESEARCH IT ON YOUTUBE](https://www.youtube.com/results?search_query=flat+earth&page=&utm_source=opensearch)!

# THIS IS POSITIVE INFO! IT'S A MATTER OF PERSPECTIVE!

# THE WAR ON TERROR IS A WAR ON YOU!

## God is so kind that it is impossible to imagine His unbounded kindness

"""

    parser = argparse.ArgumentParser(
        prog='audiobible' or sys.argv[0],
        usage=extended_help() + """audiobible [-h] [-b BOOK] [-c CHAPTER] [-C CONTEXT] [-B BEFORE_CONTEXT] [-A AFTER_CONTEXT] operation [words ...]""",
        description='%(prog)s '+__version__+' - King James Version Audio Bible'
    )

    parser.add_argument(
        'operation', nargs='+', type=str,
        help="init, hear, read, find, show, words, dict, list, hub, quote, praise, sermons, path, version, help, update"
    )
    parser.add_argument(
        "-F", "--force", action='store_true',
        help="during init operation to remove existing data before new crawl operation"
    )
    parser.add_argument("-a", "--algorithm", choices=['regex', 'ratio', 'partial', 'sort', 'set'])
    parser.add_argument("-b", "--book", type=str, help="book to hear, read, find or quote", default=None)
    parser.add_argument("-c", "--chapter", type=str, help="chapter to hear, read, find or quote", default=None)
    parser.add_argument(
        "-C", "--context", type=int,
        help="print num lines of leading and trailing context surrounding each match.", default=None
    )
    parser.add_argument(
        "-B", "--before-context", type=int, help="print num lines of trailing context before each match.", default=None
    )
    parser.add_argument(
        "-A", "--after-context", type=int,
        help="print num lines of trailing context after each match.", default=None
    )
    parser.add_argument("-s", "--speaker", type=str, help="speaker to hear a sermon from", default=None)
    parser.add_argument("-t", "--topic", type=str, help="topic to hear a sermon on", default=None)
    parser.add_argument(
        "-w", "--word", type=str, help="word to show a definition for or all words if a letter is given", default=None
    )
    parser.add_argument("-v", "--verse", type=str, help="verse to show", default=None)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    from kjv import settings

    git_repo = 'git@github.com:AudioBible/KJV.git'

    bot_name = settings.BOT_NAME

    base_path = os.environ.get('BOOKS_PATH', None)
    if not base_path:
        base_path = os.path.expanduser('~')

    data_path = os.path.join(os.path.abspath(base_path), settings.DATA_STORE)
    content_path = os.path.join(data_path, settings.CONTENT_FILE)
    speakers_path = os.path.join(data_path, settings.SPEAKERS_FILE)
    topics_path = os.path.join(data_path, settings.TOPICS_FILE)
    words_path = os.path.join(data_path, settings.DICTIONARY_FILE)
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
        from scrapy.crawler import CrawlerProcess
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
        from kjv.bible.bible import BibleSpider
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
        Download._bible()

    @staticmethod
    def speakers():
        from scrapy.crawler import CrawlerProcess
        pipelines = {
            bot_name + '.pipelines.SpeakerPipeline': 1,
        }
        spider_module = bot_name + '.speakers'
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
        from kjv.speakers.speakers import SpeakersSpider
        process.crawl(
            crawler_or_spidercls=SpeakersSpider,
        )
        process.start()

    @staticmethod
    def topics():
        from scrapy.crawler import CrawlerProcess
        pipelines = {
            bot_name + '.pipelines.TopicPipeline': 1,
        }
        spider_module = bot_name + '.topics'
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
        from kjv.topics.topics import TopicsSpider
        process.crawl(
            crawler_or_spidercls=TopicsSpider,
        )
        process.start()

    @staticmethod
    def words():
        from scrapy.crawler import CrawlerProcess
        pipelines = {
            bot_name + '.pipelines.DictionaryPipeline': 1,
        }
        spider_module = bot_name + '.dictionary'
        process = CrawlerProcess({
            'BOT_NAME': bot_name,
            'SPIDER_MODULES': settings.SPIDER_MODULES,
            'NEWSPIDER_MODULE': spider_module,
            'USER_AGENT': settings.USER_AGENT,
            'ROBOTSTXT_OBEY': settings.ROBOTSTXT_OBEY,
            'ITEM_PIPELINES': pipelines,
            'DATA_STORE': data_path,
            'DICTIONARY_FILE': settings.DICTIONARY_FILE
        })
        from kjv.dictionary.dictionary import DictionarySpider
        process.crawl(
            crawler_or_spidercls=DictionarySpider,
        )
        process.start()


class AudioBible(object):
    languages = ['hebrew', 'greek']
    book_names = {}
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
    param1 = None
    param2 = None
    word = None
    speakers = {}
    topics = {}
    words_data = {}

    def __init__(self, operation, force, algorithm, book, chapter, speaker, topic, word, context, before_context, after_context):
        function = operation[0] if operation[0].lower() in [
            'init', 'hear', 'read', 'list', 'show', 'find', 'quote', 'words', 'hub',
            'path', 'praise', 'sermon', 'sermons', 'dict', 'version', 'help', 'update', 'upgrade', 'exit'
        ] else 'help'

        if 'version' in function:
            sys.stdout.write('%s\r\n' % __version__)
            sys.exit(0)

        if 'update' in function:
            self.update()
            sys.exit(0)

        if 'exit' in function:
            self.exit()
            sys.exit(0)

        if 'init' in function or 'list' in function:
            self.scope = operation[1] if len(operation) > 1 else None
            self.force = force

        if 'dict' in function or 'words' in function:
            self.word = operation[1] if len(operation) > 1 else word

        proceed = True

        if algorithm in ['regex', 'ratio', 'partial', 'sort', 'set']:
            self.algorithm = algorithm
        else:
            self.algorithm = DEFAULT_ALGORITHM

        if function in 'words':
            self._load_words()
            self.result = self.words()
            proceed = False

        if proceed and function not in ['init', 'load', 'help', 'praise', 'dict']:
            self._load_books()
            if function in ['sermons', 'list']:
                if 'speakers' in self.scope:
                    self._load_speakers()
                if 'topics' in self.scope:
                    self._load_topics()
                if 'words' in self.scope:
                    self._load_words()
            self._set(operation, book, chapter, speaker, topic)
            if not self.book and function not in ['sermons']:
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

    def _load_words(self):
        self.words_data = {
            'all': dict(zip(list(string.ascii_uppercase), [
                [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], [], [], [], [], [],
            ])),
            'hebrew': dict(zip(list(string.ascii_uppercase), [
                [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], [], [], [], [], [],
            ])),
            'greek': dict(zip(list(string.ascii_uppercase), [
                [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], [], [], [], [], [],
            ]))
        }
        letters = string.ascii_uppercase
        for language in ['all', 'hebrew', 'greek']:
            for l in range(len(letters)):
                path = words_path % (language, letters[l])
                if os.path.exists(path):
                    with open(path, 'r') as lines:
                        for line in lines:
                            data = json.loads(line)
                            if data['letter'] == letters[l]:
                                self.words_data[language][letters[l]].append(data)
        return self.words_data

    def _set(self, operation, book, chapter, speaker, topic):
        try:
            self.book = self._valid('book', operation[1])
        except (IndexError, BookNotFoundError):
            if book:
                self._valid_book(operation, book)
        try:
            self.chapter = self._valid('chapter', operation[2])
        except (IndexError, ValueError, TypeError, ChapterNotFoundError):
            if chapter:
                self._valid_chapter(operation, chapter)
        if speaker:
            self.param1 = speaker
        elif len(operation) > 2:
            self.param1 = operation[2]
        if topic:
            self.param2 = topic
        elif len(operation) > 3:
            self.param2 = operation[3]
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
                    sys.stdout.write('Book: %s\r\nChapters: %s\r\n' % (
                        self.get_book(), [
                            self.books[x]['chapters_count']
                            for x in range(len(self.books)) if self.books[x]['name'] == self.get_book()
                        ][0]
                    ))
                    sys.exit('%s: %s' % (e.message, the_chapter))
        except IndexError:
            self.chapter = DEFAULT_CHAPTER

    def _valid(self, name, value):
        if name is 'book':
            found = None
            for bdx in range(len(self.books)):
                book = str(value).upper().replace(' ', '_')
                if book == self.books[bdx]['name'][0:len(book)]:
                    found = self.books[bdx]['name']
                else:
                    match = re.search(book, self.books[bdx]['name'].replace(' ', '_'), re.IGNORECASE)
                    if match:
                        found = match.string

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

    def init(self):
        if not self.scope:
            if self.force and os.path.exists(content_path):
                os.remove(content_path)
            return Download.init()
        elif self.scope in 'bible':
            if self.force and os.path.exists(data_path):
                import shutil
                for dirname, dirnames, filenames in os.walk(data_path):
                    for name in dirnames:
                        if name not in ['.git', 'speakers', 'topics', 'words']:
                            shutil.rmtree(os.path.join(dirname, name))
            return Download.load()
        elif self.scope in 'speakers' or self.scope in 'preachers':
            if self.force and os.path.exists(data_path):
                if os.path.exists(os.path.dirname(speakers_path)):
                    import shutil
                    shutil.rmtree(os.path.dirname(speakers_path))
            return Download.speakers()
        elif self.scope in 'topics':
            if self.force and os.path.exists(data_path):
                if os.path.exists(os.path.dirname(topics_path)):
                    import shutil
                    shutil.rmtree(os.path.dirname(topics_path))
            return Download.topics()
        elif self.scope in 'words':
            if self.force and os.path.exists(data_path):
                if os.path.exists(os.path.dirname(words_path)):
                    import shutil
                    shutil.rmtree(os.path.dirname(words_path))
            return Download.words()
        elif self.scope in 'git':
            def clone(repo, path):
                subprocess.check_output("git clone %s %s" % (repo, path), shell=True)

            import subprocess
            if os.path.exists(data_path):
                if self.force:
                    import shutil
                    shutil.rmtree(data_path)
                    clone(git_repo, data_path)
                else:
                    sys.stdout.write(
                        "Data path exists: %s\r\n"
                        "If you want to remove the directory and start over type:\r\n"
                        "audiobible init git -F\r\n" % data_path
                    )
            else:
                clone(git_repo, data_path)

    def _open(self, filepath):
        import subprocess
        if sys.platform.startswith('darwin'):
            if 'rm ' not in filepath and ';' not in filepath and '|' not in filepath:
                subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            if 'rm ' not in filepath and ';' not in filepath and '|' not in filepath:
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

    def hub(self):
        if self.get_book() and self.get_chapter():
            self._open("http://biblehub.com/interlinear/%s/%s.htm" % (self.get_book().lower(), self.get_chapter()))
        elif self.get_book():
            self._open("http://biblehub.com/interlinear/%s/1.htm" % self.get_book().lower())
        else:
            self._open("http://biblehub.com")

    def dict(self):
        if self.word:
            match = re.search('([H,G])([0-9]).*', self.word, re.IGNORECASE)
            if match:
                self._open("http://www.kingjamesbibledictionary.com/StrongsNo/%s" % self.word.upper())
            else:
                self._open("http://www.kingjamesbibledictionary.com/Dictionary/%s" % self.word)
        else:
            self._open("http://www.kingjamesbibledictionary.com/Dictionary/")

    def words(self):
        def get_data(word):
            data = ''
            lang = None
            if 'strongs_number' in word:
                if 'H' in word['strongs_number']:
                    lang = 'Hebrew'
                elif 'G' in word['strongs_number']:
                    lang = 'Greek'
                else:
                    pass

                if word['strongs_number']:
                    data += 'Strong\'s No: %s\r\n' % word['strongs_number']

            if 'word_original' in word and word['word_original']:
                data += '%s: %s\r\n' % (lang, word['word_original'])
            if 'word_translated' in word and word['word_translated']:
                data += 'English: %s\r\n' % word['word_translated']
            if 'transliteration' in word and word['transliteration']:
                data += 'Transliteration: %s\r\n' % word['transliteration']
            if 'phonetic' in word and word['phonetic']:
                data += 'Phonetic: %s\r\n' % word['phonetic']
            if 'word_origin' in word and word['word_origin']:
                data += 'Word Origin: %s\r\n\r\n' % word['word_origin']
            if 'bible_usage' in word and word['bible_usage']:
                data += 'Bible Usage:\r\n    %s\r\n\r\n' % word['bible_usage']
            if 'part_of_speech' in word and word['part_of_speech']:
                data += 'Part of Speech:\r\n    %s\r\n\r\n' % word['part_of_speech']
            if 'strongs_definition' in word and word['strongs_definition']:
                data += 'Strong\'s Definition:\r\n    %s\r\n\r\n' % word['strongs_definition']
            if 'thayers_definition' in word and word['thayers_definition']:
                data += 'Thayer\'s Definition:\r\n    %s\r\n\r\n' % word['thayers_definition']
            if 'brown_driver_definition' in word and word['brown_driver_definition']:
                data += 'Brown Driver Definition:\r\n    %s\r\n\r\n' % "\r\n    ".join(
                    [w.strip() for w in word['brown_driver_definition']]
                )
            if 'translation_occurrences' in word and word['translation_occurrences']:
                data += 'Translation Occurrences:\r\n    %s\r\n\r\n' % ", ".join([
                    "%s: %s" % (w, word['translation_occurrences'][w])
                        for w in word['translation_occurrences'].keys()
                ])
            if 'bible_references' in word and word['bible_references']:
                data += 'Bible References:\r\n    %s\r\n' % ", ".join(word['bible_references'])

            nums = word['data'].keys()
            nums.sort()
            for wdx in range(len(nums)):
                if 'Word' in word['data'][nums[wdx]] and \
                        'Definitions' in word['data'][nums[wdx]] and \
                        'Dictionary' in word['data'][nums[wdx]]:
                    data += "\r\n%s:\r\n" % word['data'][nums[wdx]]['Dictionary']
                    data += "    %s\r\n\r\n" % word['data'][nums[wdx]]['Word']
                    data += 'Definition:\r\n    %s\r\n' % "\r\n    ".join(word['data'][nums[wdx]]['Definitions'])
            data += '\r\n===\r\n\r\n'
            return data

        result = ''

        if self.word:
            for language in self.languages:
                for letter in string.ascii_uppercase:
                    for word in self.words_data[language][letter]:
                        match_numr = re.search('([H,G])([0-9]).*', self.word, re.IGNORECASE)
                        # match_word = re.search(self.word, word['word_translated'], re.IGNORECASE)
                        if match_numr:
                            if match_numr.string.upper() == word['strongs_number'].upper():
                                result += get_data(word)
                        elif self.word.upper() == word['word_translated'].upper():
                            result += get_data(word)
        else:
            for language in self.languages:
                for letter in string.ascii_uppercase:
                    for word in self.words_data[language][letter]:
                        result += get_data(word)

        result = result.strip().strip('===')
        return result

    def sermons(self):
        if self.param1:
            speaker = "&subsetCat=speaker&subsetItem=%s" % self.param1
        else:
            speaker = ''

        if speaker and not self.param2:
            if self.get_book():
                if not isinstance(self.get_chapter(), list):
                    chapter = self.get_chapter()
                else:
                    chapter = ''
                self._open(
                    "http://www.sermonaudio.com/search.asp?BibleOnly=true&keyword=%s&chapter=%s%s" %
                    (self.get_book(), chapter, speaker))
            else:
                self._open(
                    "http://www.sermonaudio.com/search.asp?speakeronly=true&currsection=sermonsspeaker&keyword=%s" % self.param1.replace(' ', '_')
                )
        elif self.param2:
            topic = self.param2
            self._open(
                "http://www.sermonaudio.com/search.asp?keywordDesc=%s&keyword=%s%s" %
                (topic, topic, speaker)
            )
        else:
            self._open("http://sermonaudio.com")

    def update(self):
        import subprocess
        subprocess.call(('pip', 'install', '--upgrade', 'audiobible'))
        return self

    def exit(self):
        import subprocess
        pids = subprocess.check_output("ps aux | grep audiobible|grep -v grep|awk '{print $2}'", shell=True)
        pids = pids.split()
        for pid in pids:
            if pid.strip() != str(os.getpid()):
                os.kill(int(pid.strip()), 9)

        return self

    def path(self):
        return os.path.join(data_path, self.get_book())

    def hear(self):
        audio = self.get_filenames('mp3')
        for a in audio:
            if os.path.exists(a):
                self._open(a)
            else:
                output = 'File Not Found: %s\r\n' % a
                output += "Please run this command to download it:\r\n"
                output += "audiobible init\r\n"
                output += "audiobible init bible\r\n"
                output += "or\r\n"
                output += "audiobible init git -F\r\n"
                return output

    def read(self):
        text = self.get_filenames('txt')
        for t in text:
            if os.path.exists(t):
                self._open(t)
            else:
                output = 'File Not Found: %s\r\n' % t
                output += "Please run this command to download it:\r\n"
                output += "audiobible init\r\n"
                output += "audiobible init bible\r\n"
                output += "or\r\n"
                output += "audiobible init git -F\r\n"
                return output

    def show(self):
        text = self.get_filenames('txt')
        texts = []
        for t in text:
            if os.path.exists(t):
                for l in open(t).readlines():
                    texts.append('%s\r\n' % l.strip())
            else:
                output = 'File Not Found: %s\r\n' % t
                output += "Please run this command to download it:\r\n"
                output += "audiobible init\r\n"
                output += "audiobible init bible\r\n"
                output += "or\r\n"
                output += "audiobible init git -F\r\n"
                return output
        return "\r\n".join(texts).strip()

    def _get_books(self, path):
        out = []
        for book in self.books:
            book_path = os.path.join(data_path, book['name'].replace(' ', '_'))
            if path in book_path and os.path.isdir(book_path):
                for dirname, dirnames, filenames in os.walk(book_path):
                    try:
                        numbers = [int(filter(str.isdigit, str(f).replace('1_', '').replace('2_', '').replace('3_', ''))) for f in filenames if '.txt' in f]
                    except:
                        numbers = [int("".join(list(filter(str.isdigit, str(f).replace('1_', '').replace('2_', '').replace('3_', ''))))) for f in filenames if '.txt' in f]

                    numbers.sort()
                    if numbers:
                        digit = int("".join(list(filter(str.isdigit, str(filenames[0].replace('.mp3', '.txt')).replace('1_', '').replace('2_', '').replace('3_', '')))))
                        for num in numbers:
                            filename = filenames[0].replace('.mp3', '.txt').replace(str(digit), str(num))
                            out.append(os.path.join(dirname, filename))
        return out

    def get_lines(self, the_path, callback):
        lines = []

        def _get_lines(path):
            if os.path.exists(path):
                if os.path.isdir(path):
                    for filename in self._get_books(path):
                        if '.txt' in filename and os.path.exists(filename):
                            # book_name = os.path.split(os.path.dirname(filename))[1].replace('_', ' ')
                            for l in open(filename).readlines():
                                if l.strip():
                                    # line = "%s %s" % ("_".join(book_name.split()), " ".join(l.strip().split(' ')[1:]))
                                    lines.append('%s\r\n' % l.strip())
                else:
                    if '.txt' in path and os.path.exists(path):
                        # book_name = os.path.split(os.path.dirname(path))[1].replace('_', ' ')
                        for l in open(path).readlines():
                            if l.strip():
                                # line = "%s %s" % ("_".join(book_name.split()), " ".join(l.strip().split(' ')[1:]))
                                lines.append('%s\r\n' % l.strip())

        if isinstance(the_path, list):
            for p in the_path:
                _get_lines(p)
        else:
            _get_lines(the_path)

        callback(lines)

    def _get_text(self, type, context, before, after):
        if not self.books:
            output = "No books found. Please run these commands to download them:\r\n"
            output += "audiobible init\r\n"
            output += "audiobible init bible\r\n"
            output += "or\r\n"
            output += "audiobible init git -F\r\n"
            return output
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
                    def matched(found):
                        if before:
                            for num in range(int(before), 0, -1):
                                try:
                                    verse = lines[line - num]
                                    if verse not in output:
                                        output.append(verse)
                                except IndexError:
                                    pass

                        verse = found
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

                    # if ':' in self.query:
                    #     query_list = self.query.split()
                    #     book_name = query_list[0]
                    #     try:
                    #         scripture = query_list[1]
                    #     except IndexError:
                    #         scripture = ''
                    #     if scripture in [lines[line].split()[1]] and book_name.upper() in lines[line]:
                    #         matched(lines[line])
                    # else:
                    match = re.search(self.query, lines[line], re.IGNORECASE)
                    if match:
                        matched(match.string)

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
                    import random
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
                output = "No Data Found. Please run these commands to download:\r\n"
                output += "audiobible init\r\n"
                output += "audiobible init bible\r\n"
                output += "or\r\n"
                output += "audiobible init git -F\r\n"
                return output

        return str("\r\n".join([o for o in output if o])).strip()

    def find(self, context, before, after):
        return self._get_text('find', context, before, after)

    def list(self):
        output = ''
        if not self.scope or self.scope in 'books':
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
                output += "audiobible init bible\r\n"
                output += "or\r\n"
                output += "audiobible init git -F\r\n"
                # output += "audiobible load\r\n"
        elif self.scope in 'speakers':
            if len(self.speakers['A']) > 0:
                for k in self.speakers.keys():
                    for s in self.speakers[k]:
                        if self.param1:
                            match = re.search(
                                self.param1,
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
                output += 'or\r\n'
                output += 'audiobible init git -F\r\n'
        elif self.scope in 'topics':
            found = False
            if len(self.topics['A']) > 0:
                def matcher(param, data):
                    match = re.search(
                        param,
                        data,
                        re.IGNORECASE
                    )
                    if match:
                        return "%s\r\n" % match.string
                    else:
                        return False

                for k in self.topics.keys():
                    if not found:
                        for t in self.topics[k]:
                            if self.param1:
                                data = matcher(self.param1, t['name'])
                                if data:
                                    found = True
                                    output += data
                            else:
                                found = True
                                output += "%s\r\n" % t["name"]
            else:
                output = 'No topics found. Please run this command to download them:\r\n'
                output += 'audiobible init topics\r\n'
                output += 'or\r\n'
                output += 'audiobible init git -F\r\n'
        elif self.scope in 'words':
            all_words = {}
            for lang in self.languages:
                if len(self.words_data[lang]) > 0:
                    for letter in self.words_data[lang].keys():
                        for s in self.words_data[lang][letter]:
                            all_words[s['word_translated']] = s['strongs_number']
            words = all_words.keys()
            words.sort()
            for wdx in range(len(words)):
                if self.param1:
                    if self.param1.upper() in words[wdx].upper():
                        output += '{:<10}{}\r\n'.format(all_words[words[wdx]], words[wdx])
                    elif self.param1.upper() == all_words[words[wdx]]:
                        output += '{:<10}{}\r\n'.format(all_words[words[wdx]], words[wdx])
                else:
                    output += '{:<10}{}\r\n'.format(all_words[words[wdx]], words[wdx])
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
        force=None,
        algorithm=None,
        book=None,
        chapter=None,
        speaker=None,
        topic=None,
        word=None,
        context=None,
        before_context=None,
        after_context=None
    ):
        try:
            return AudioBible(
                operation=operation,
                force=force,
                algorithm=algorithm,
                book=book,
                chapter=chapter,
                speaker=speaker,
                topic=topic,
                word=word,
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
            force=args.force,
            algorithm=args.algorithm,
            book=args.book,
            chapter=args.chapter,
            speaker=args.speaker,
            topic=args.topic,
            word=args.word,
            context=args.context,
            before_context=args.before_context,
            after_context=args.after_context
        )
    # dict arguments
    if isinstance(kwargs, dict):
        return use_params(
            operation=kwargs.get('operation'),
            force=kwargs.get('force'),
            algorithm=kwargs.get('algorithm'),
            book=kwargs.get('book'),
            chapter=kwargs.get('chapter'),
            speaker=kwargs.get('speaker'),
            topic=kwargs.get('topic'),
            word=kwargs.get('word'),
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
    try:
        result = use_parse_args()
        if result:
            sys.stdout.write("%s\r\n" % str(result.encode('utf-8')).strip())
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
