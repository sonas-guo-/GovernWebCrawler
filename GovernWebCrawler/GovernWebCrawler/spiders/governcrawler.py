# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse,Request,FormRequest
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from urllib.parse import urlparse,urlsplit,urljoin
from GovernWebCrawler.items import GovernwebcrawlerItem
from GovernWebCrawler.utils import load_domains,load_tags,load_websites,get_schemenetloc
import urllib.request
import json
import re
import io
import os

class GovernCrawler(CrawlSpider):
    name='govern_crawler'
    allowed_domains = []
    tags=[]
    websites={}
    def __init__(self):
        domains=load_domains()
        self.allowed_domains.extend(domains)
        tags=load_tags()
        self.tags.extend(tags)
        self.websites=load_websites()
        #print(self.websites)
    def start_requests(self):
        urls=[
            ]
        for key,value in self.websites.items():
            #pass
            urls.append(key)
            urls.extend(value['complements'])

        for url in urls:
            req=Request(url=url,callback=self.parse)
            if not url.endswith('.html'):
                req.meta['PhantomJS'] = True
            yield req

    def parse(self,response):
        curr_url=response.url
        key=get_schemenetloc(curr_url)
        if key in self.websites:
            rule=self.websites[key]
            item=ItemLoader(item=GovernwebcrawlerItem(),response=response)
            root=rule['root_div']
            title=rule['title']
            content=rule['content']
            time=rule['time']
            desc=rule['desc']
            item.add_xpath('title',root+title)
            item.add_xpath('time',root+time)
            item.add_xpath('content',root+content)
            item.add_value('url',curr_url)
            item.add_value('desc',desc)
            
            yield item.load_item()
         
        body=response.body
        content=body.decode('utf8',errors='ignore')

        results=Selector(text=content).xpath('//a').extract()
        for res in results:
            sel=Selector(text=res)
            url=sel.xpath('//a/@href').extract()
            name=sel.xpath('//a/text()').extract()
            if len(url)!=0:
                url=urljoin(curr_url, url[0])
                req=Request(url=url,callback=self.parse)
                if not url.endswith('.html'):
                    req.meta['PhantomJS'] = True
                yield req
        
