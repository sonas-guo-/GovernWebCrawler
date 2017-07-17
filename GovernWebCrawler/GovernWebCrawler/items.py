# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose ,Compose
from w3lib.html import remove_tags
from GovernWebCrawler.utils import load_timefmts

import re
def keep_time(element):
    timefmts=load_timefmts()
    pattern=re.compile(timefmts)
    matches=pattern.search(element)
    if matches:
        return matches.group(1)
def remove_symbols(element):
    lst=element.split()
    res=''.join(lst)
    return res

def replace_SBCspace(element):
    return element.replace('\u3000',' ')
class GovernwebcrawlerItem(scrapy.Item):
    url=scrapy.Field()
    desc=scrapy.Field()
    time=scrapy.Field(
        input_processor=MapCompose(remove_tags,replace_SBCspace,keep_time)
    )
    title=scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    content=scrapy.Field(
        input_processor=MapCompose(remove_tags,remove_symbols)
    )
    #input()
