# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class TopicContentItem(scrapy.Item):
	topic_id = scrapy.Field()
	topic_headline = scrapy.Field()
	topic_author = scrapy.Field()
	topic_author_id = scrapy.Field()
	topic_time = scrapy.Field()
	topic_content = scrapy.Field()
	topic_like = scrapy.Field()
	reply_count = scrapy.Field()
class TopicRemarkItem(scrapy.Item):
	remark_num_id = scrapy.Field()
	topic_id = scrapy.Field()
	remark_id = scrapy.Field()
	remark_by = scrapy.Field()
	remark_content = scrapy.Field()
	remark_time = scrapy.Field()
