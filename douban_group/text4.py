import requests
import re
from bs4 import BeautifulSoup
response = requests.get('https://www.douban.com/group/topic/98388480/?start=300')
soup = BeautifulSoup(response.text,'lxml')
ul = soup.find('ul',class_='topic-reply',id="comments")
reply_list = ul.find_all('li')
for ele in reply_list:
	parti = ele.find("h4").find('a')
	parti_id = re.split('/',parti['href'])[4]
	parti_name = parti.string
	reply_time = ele.find('h4').find('span').get_text()
	reply_content = ele.find('p').string
	print("参与人ID:(%s) 参与人昵称：(%s)回复时间：(%s)回复内容：(%s)"%(parti_id,parti_name,reply_time,reply_content))

print(type(ul))
#next_ = soup.find('div',class_='paginator').find('span',class_='next').a
#if next_ is None:
#	print('null link')
