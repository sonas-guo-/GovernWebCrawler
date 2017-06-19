# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import sqlite3
import os

class GovernwebcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class Sqlite3Pipeline(object):
    def __init__(self,db_dir,db_name,db_tablename):
        self.tablename=db_tablename
        self.crawled_urls=set()
        if not os.path.exists(db_dir):
            os.mkdir(db_dir)
        db=db_dir+'/'+db_name
        self.conn = sqlite3.connect(db)
        self.create_table(db_tablename)
        self.read_exists()
    def read_exists(self):
        
        select_cmd='''
        select url from %s
        '''%(self.tablename)
        #print(select_cmd)
        c=self.conn.cursor()
        res=c.execute(select_cmd)
        for url in res:
            self.crawled_urls.add(url)
            
    def create_table(self,db_tablename):
        try:
            create_tb_cmd='''
            CREATE TABLE %s(
            url text,
            time text,
            title text,
            content text            
            )
            '''%(db_tablename)
            self.conn.execute(create_tb_cmd)    
        except Exception as e:
            print(e)
    
    def process_item(self, item, spider):
        #print(item)
        if 'url' in item and len(item['url'])>0:
            url=item['url'][0]
        else:
            raise DropItem('item缺少链接')

        if url in self.crawled_urls:
            raise DropItem('%s 该页面已被爬取'%url)

        if 'time' in item and len(item['time'])>0:
            time=item['time'][0]
        else:
            raise DropItem('item缺少时间')
        if 'title' in item and len(item['title'])>0:
            title=item['title'][0]
        else:
            raise DropItem('item缺少标题')
        if 'content' in item and len(item['content'])>0:
            content=item['content'][0]
        else:
            raise DropItem('item缺少内容')
        
        insert_cmd='''
        insert into %s values(
        '%s','%s','%s','%s'
        )
        '''%(self.tablename,url,time,title,content)

        c=self.conn.cursor()
        c.execute(insert_cmd)
        self.conn.commit()
        print('%s write db done!'%url)
        self.crawled_urls.add(url)
        
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            db_dir=crawler.settings.get('SQLITE_DIR'),
            db_name=crawler.settings.get('SQLITE_FILE'),
            db_tablename=crawler.settings.get('SQLITE_TABLE')
            )
    def open_spider(self,spider):
        pass
    def close_spider(self,spider):
        self.conn.close()
