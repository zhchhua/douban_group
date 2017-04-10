import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.http import Request
from douban_group.items import TopicContentItem
from douban_group.items import TopicRemarkItem
from douban_group.mysqlpipelines.sql import Sql
import random
class Myspider(scrapy.Spider):
    name = 'kaopu'
    urls = 'http://www.douban.com/group/kaopulove/discussion?start='
    def start_requests(self):
        for i in range(0,68500,25):
            url = self.urls + str(i)
            yield Request(url,meta={'proxy_index':0},callback = self.parse0)
    def parse0(self,response):
        if response.status != 200:
            req = response.request
            req.meta['change_proxy'] = True
            yield req
        else:    
            table = BeautifulSoup(response.text,'lxml').find('table',class_='olt')
            tr_list = table.find_all('td',class_="title")
            remark_num = 0
            for td in tr_list:
                topic_url = td.find('a')
                print("网址链接 %s"%(topic_url['href']))
                count = topic_url.parent.next_sibling.next_sibling.next_sibling.next_sibling.text
                if count == None:
                    count = 0
                url = topic_url['href']
                yield Request(url,callback = self.parse1,meta ={"proxy_index":0,"count" : count})
    def parse1(self,response):
        if response.status != 200:
            req = response.request
            req.meta['change_proxy'] = True
            yield req
        else:    
            topic_item = TopicContentItem()
            soup = BeautifulSoup(response.text,'lxml')
            topic_id = re.match(r'(.*?)/(\d+)/(.*?)',response.url).group(2)
            headline = soup.h1.get_text()
            user_link = soup.find('div',class_="topic-content clearfix").find('span',class_="from").find('a')
            user_id = re.match(r'(.*?)/people/(.*?)/',user_link['href']).group(2)
            user_name = user_link.text
            pub_time = soup.find('div',class_ = 'topic-doc').find('span',class_='color-green').text
            if soup.find('div',class_ ='topic-content clearfix').find('div','topic-content').p != None:
                topic_content = soup.find('div',class_ ='topic-content clearfix').find('div','topic-content').p.get_text().strip()
            else:
                topic_content = ""
            topic_like = soup.find('span',class_='fav-num')
            reply_count = response.meta['count']
            topic_item['topic_id'] = topic_id
            topic_item['topic_headline'] = headline
            topic_item['topic_author_id'] = user_id
            topic_item['topic_author'] = user_name
            topic_item['topic_time'] = pub_time
            if topic_like is None:
                topic_item['topic_like'] = 0
            else:
                topic_item['topic_like'] = topic_like.find('a').text
            topic_item['topic_content'] = str(topic_content)
            topic_item['reply_count'] =reply_count
            yield topic_item
            reply_list = soup.find('ul',class_="topic-reply").find_all('li')
            remark_num = 0 
            for ele in reply_list:
                topic_remark_item = TopicRemarkItem()
                parti = ele.find("h4").find('a')
                parti_id = re.split('/',parti['href'])[4]
                parti_name = parti.text
                reply_time = ele.find('h4').find('span').get_text()
                reply_content = ele.find('p').text
                topic_remark_item['remark_num_id'] = remark_num
                remark_num = remark_num+1
                topic_remark_item['topic_id'] = topic_id
                topic_remark_item['remark_id'] = parti_id
                topic_remark_item['remark_by'] = parti_name
                topic_remark_item['remark_time'] = reply_time
                topic_remark_item['remark_content'] = reply_content
                yield topic_remark_item
            has_next = soup.find('div',class_='paginator')
            if has_next != None:
                if has_next.find('span',class_='next').a != None:
                    yield Request(has_next.find('span',class_='next').a['href'],meta={"proxy_index":0,"remark_num":remark_num},callback = self.parse2)
    def parse2(self,response):
        if response.status != 200:
            req = response.request
            req.meta['change_proxy'] = True
            yield req
        else:
            soup = BeautifulSoup(response.text,'lxml')
            topic_id = re.match(r'(.*?)/(\d+)/(.*?)',response.url).group(2)
            ul = soup.find('ul',class_='topic-reply',id="comments")
            reply_list = ul.find_all('li')
            remark_num = int(response.meta['remark_num']) + 1
            for ele in reply_list:
                topic_remark_item = TopicRemarkItem()
                parti = ele.find("h4").find('a')
                parti_id = re.split('/',parti['href'])[4]
                parti_name = parti.text
                reply_time = ele.find('h4').find('span').get_text()
                reply_content = ele.find('p').text
                topic_remark_item['remark_num_id'] = remark_num
                remark_num = remark_num+1
                topic_remark_item['topic_id'] = topic_id
                topic_remark_item['remark_id'] = parti_id
                topic_remark_item['remark_by'] = parti_name
                topic_remark_item['remark_time'] = reply_time
                topic_remark_item['remark_content'] = reply_content
                yield topic_remark_item
            has_next = soup.find('div',class_='paginator')
            if has_next != None:
                if has_next.find('span',class_='next').a != None:
                    yield Request(has_next.find('span',class_='next').a['href'],meta={"proxy_index":0,"remark_num":remark_num},callback = self.parse2)
	







	







