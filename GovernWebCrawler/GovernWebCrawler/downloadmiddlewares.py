# -*- encoding:utf8 -*-
from scrapy.http import HtmlResponse
from selenium import webdriver

class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        ptjs=spider.settings.get('PHANTOMJS_PATH')
        if 'PhantomJS' in request.meta:
            driver = webdriver.PhantomJS(executable_path=ptjs)
            driver.get(request.url)
            content = driver.page_source.encode('utf-8')
            driver.quit()  
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
