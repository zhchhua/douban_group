from .sql import Sql
from douban_group.items import TopicContentItem
from douban_group.items import TopicRemarkItem

class DouBanGroupPipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,TopicContentItem):
            id = item['topic_id']
            ret = Sql.select_topic(id)
            if ret[0] == 1:
                print('已存在')
                pass
            else:
                headline = item['topic_headline']
                author = item['topic_author']
                author_id = item['topic_author_id']
                pub_time = item['topic_time']
                content = item['topic_content']
                like = item['topic_like']
                count = item['reply_count']
                Sql.insert_topic(id,headline,author,author_id,pub_time,content,like,count)
                print("开始保存话题")
        if isinstance(item,TopicRemarkItem):
            num_id = item['remark_num_id']
            topic_id = item['topic_id']
            ret = Sql.select_reply(num_id,topic_id)
            if ret[0] == 1:
                print('已存在')
                pass
            else:
                user_id = item['remark_id']
                user_name = item['remark_by']
                remark_content = item['remark_content']
                remark_time = item['remark_time']
                Sql.insert_topic_reply(num_id,topic_id,user_id,user_name,remark_content,remark_time)
                print('保存评论')
