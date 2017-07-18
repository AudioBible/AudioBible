import os
from kjv import settings

bot_name = settings.BOT_NAME
base_path = os.environ.get('BOOKS_PATH', None)
if not base_path:
    base_path = os.path.expanduser('~')

data_path = os.path.join(os.path.abspath(base_path), settings.DATA_STORE)


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