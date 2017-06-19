# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose ,Compose
from w3lib.html import remove_tags
def keep_time(element):
    content=element.strip()
    if '时间' in content:
        return content
def remove_symbols(element):
    lst=element.split()
    res=''.join(lst)
    return res
class GovernwebcrawlerItem(scrapy.Item):
    url=scrapy.Field()
    time=scrapy.Field(
        input_processor=MapCompose(remove_tags,keep_time)
    )
    title=scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    content=scrapy.Field(
        input_processor=MapCompose(remove_tags,remove_symbols)
    )
    #print(url,time,titile,content)
    
