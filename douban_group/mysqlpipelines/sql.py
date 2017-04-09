import mysql.connector
from douban_group import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD =settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB
con = mysql.connector.connect(user = MYSQL_USER,password = MYSQL_PASSWORD,host =MYSQL_HOSTS,database = MYSQL_DB)
cur = con.cursor(buffered = True)

class Sql:	
	@classmethod
	def insert_topic(cls,id,headline,author,author_id,pub_time,content,like,count):
		sql = 'INSERT INTO kaopu_topic(`id`,`headline`,`author`,`author_id`,`pub_time`,`content`,`like`,`count`) values (%(id)s,%(headline)s,%(author)s,%(author_id)s,%(pub_time)s,%(content)s,%(like)s,%(count)s)'
		value = {
			'id':id,
			'headline':headline,
			'author':author,
			'author_id':author_id,
			'pub_time':pub_time,
			'content':content,
			'like':like,
			'count':count
			}
		cur.execute(sql,value)
		con.commit()
	@classmethod
	def insert_topic_reply(cls,num_id,topic_id,user_id,user_name,remark_content,remark_time):
		sql = 'INSERT INTO kaopu_topic_reply (`num_id`,`topic_id`,`user_id`,`user_name`,`remark_content`,`remark_time`) VALUES (%(num_id)s,%(topic_id)s,%(user_id)s,%(user_name)s,%(remark_content)s,%(remark_time)s)'
		value ={
			'num_id':num_id,
			'topic_id':topic_id,
			'user_id':user_id,
			'user_name':user_name,
			'remark_content':remark_content,
			'remark_time':remark_time
		}
		cur.execute(sql,value)
		con.commit()
	@classmethod
	def select_topic(cls,id):
		sql = "SELECT EXISTS( SELECT 1 FROM kaopu_topic WHERE id=%(id)s)"
		value = {'id':id}
		cur.execute(sql,value)
		return cur.fetchall()[0]
	@classmethod
	def select_reply(cls,num_id,topic_id):
		sql = "SELECT EXISTS( SELECT 1 FROM kaopu_topic_reply WHERE num_id=%(num_id)s and topic_id=%(topic_id)s)"
		value ={
			"num_id":num_id,
			"topic_id":topic_id
		}
		cur.execute(sql,value)
		return cur.fetchall()[0]
