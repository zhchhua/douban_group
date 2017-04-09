import requests
import re
from bs4 import BeautifulSoup
response = requests.get('https://www.douban.com/group/topic/91554354/')
print(response.url)
con = BeautifulSoup(response.text,'lxml')
headline= con.find('div',id="content")
user= con.find('div',class_="topic-content clearfix").find('div',class_="user-face").find('a')
user_name = user.string
topic_time = con.find('div',class_ = 'topic-doc').find('span',class_='color-green')
topic_time = topic_time.get_text()
topic_content = con.find('div',class_ ='topic-content clearfix').find('div','topic-content').p
topic_content = topic_content.get_text().strip()
print("标题:%s	用户id：%s	发表时间：%s	"%(con.h1.get_text().strip(),re.match(r'(.*?)/(\d+)/',user['href']).group(2),topic_time))
print("主题内容:%s"%topic_content)
#print(re.match(r'people/(\d+)/',str(user[0])).group(1))
#user_id = re.split('/',str(a['href']))[4]
#print(user_id)
reply =con.find('ul',class_='topic-reply',id='comments')
reply_list = reply.find_all('li')
for ele in reply_list:
	parti = ele.find("h4").find('a')
	parti_id = re.split('/',parti['href'])[4]
	parti_name = parti.string
	reply_time = ele.find('h4').find('span').get_text()
	reply_content = ele.find('p').string
	print("参与人ID:(%s) 参与人昵称：(%s)回复时间：(%s)回复内容：(%s)"%(parti_id,parti_name,reply_time,reply_content))
