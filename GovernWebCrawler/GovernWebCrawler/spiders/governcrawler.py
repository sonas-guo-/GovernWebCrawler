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
import urllib.request
import json
import re
import io
import os
class GovernCrawler(CrawlSpider):
    name='govern_crawler'
    allowed_domains = ["jiangsu.gov.cn"]
    def gen_allowed_domains(self,urls):
        domains=[
            'jiangsu.gov.cn'
        ]
        for url in urls:
            res=urlparse(url)
            #print(res)
            #print(res.netloc)
            domains.append(res.netloc)
        return domains
    def start_requests(self):
        self.urls = [
            'http://www.jiangsu.gov.cn/',
            #'http://www.jiangsu.gov.cn/rdgz/201706/t20170617_482013.html',
            #'http://www.jiangsu.gov.cn/ttxw/201706/t20170617_482014.html',
            #'http://www.jiangsu.gov.cn/rdgz/201705/t20170518_478516.html'
        ]
        #self.allowed_domains = self.gen_allowed_domains(self.urls)
        for url in self.urls:
            #pass
            yield Request(url=url,callback=self.parse)

    def parse(self,response):
        curr_url=response.url
        #print(curr_url)
        #print(get_base_url(response))
        
        item=ItemLoader(item=GovernwebcrawlerItem(),response=response)
        root_path='//div[@class="detail"]/div[@class="L"]'
        item.add_xpath('title',root_path+'/div[@class="ttL"]/h2')
        item.add_xpath('time',root_path+'/div[@class="ttL"]/p/span[1]')
        item.add_xpath('content',root_path+'/div[@id="con"]/div[@class="TRS_Editor"]')
        item.add_value('url',curr_url)
        yield item.load_item()

        body=response.body
        content=body.decode('utf8',errors='ignore')
        results=Selector(text=content).xpath('//a').extract()
        for res in results:
            #print(res)
            sel=Selector(text=res)
            url=sel.xpath('//a/@href').extract()
            name=sel.xpath('//a/text()').extract()
            if len(url)!=0:
                url=urljoin(curr_url, url[0])
                yield Request(url, callback=self.parse)

        
