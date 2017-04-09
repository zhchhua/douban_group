import requests
import re
from bs4 import BeautifulSoup
response = requests.get('https://www.douban.com/group/kaopulove/discussion?start=0')
table = BeautifulSoup(response.text,'lxml').find('table',class_='olt')
tr_list = table.find_all('td',class_="title")
for td in tr_list:
	topic_url = td.find('a')
	count = topic_url.parent.next_sibling.next_sibling.next_sibling.next_sibling.string
	print("总回复数：%s  链接：%s"%(count,topic_url['href']))
