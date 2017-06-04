# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Spider
from scrapy.item import Field, Item, DictItem
from scrapy.loader import ItemLoader


class InvalidItemLoaderName(ValueError):
    pass


def create_item_class(class_name, field_list):
    field_dict = {}
    for field_name in field_list:
        field_dict[field_name] = Field()
    return type(str(class_name), (DictItem,), {'fields': field_dict})


def get_item_and_loader(class_obj, keys):
    class_name = ''
    if isinstance(class_obj, Spider):
        class_name = class_obj.__class__.__name__.replace('Spider', '')
    elif isinstance(class_obj, basestring):
        class_name = class_obj
    else:
        if hasattr(class_obj, 'crawler'):
            class_obj.crawler.stop()
            raise InvalidItemLoaderName('%s is not valid' % class_obj)

    base_item_class = 'DictItem'
    base_loader_class = 'ItemLoader'

    locals()['%sItem' % class_name] = create_item_class('%sItem' % class_name, keys)
# after creating the item its still now available in the loader exec so we need to place it into globals() first
    globals()['%sItem' % class_name] = locals()['%sItem' % class_name]

    if '%sLoader' % class_name not in locals().keys():
        exec """
class %sLoader(%s):
    default_item_class = %sItem

        """ % (class_name, base_loader_class, class_name)
        globals()['%sLoader' % class_name] = locals()['%sLoader' % class_name]

    #grab the loader and the item that was dynamically created and return it to the spider
    ModelLoader = locals()['%sLoader' % class_name]
    ModelItem = locals()['%sItem' % class_name]
    return ModelItem, ModelLoader

