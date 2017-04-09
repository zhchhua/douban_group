import requests
import re
from bs4 import BeautifulSoup
def has_blank_class(tag):
	return tag.get('class')==None and not tag.has_attr('id') and tag.name =='td' 

def get_user_id(tag):
	return tag.name == 'td' and not tag.has_attr('class')

def get_remarks_list(tag):
	return tag.name == 'td' and tag.has_attr('class')  
response = requests.get('http://www.douban.com/group/kaopulove/discussion?start=25')
con = BeautifulSoup(response.text,'lxml')
table = con.find('table',class_ ="olt")
topic_list = table.find_all('td',class_='title')
#id_list
#remaks_num_list
#remarks_time_list
for tr in topic_list:
	topic =tr.a.string
	#print(topic.strip())
	link = tr.a['href']
	#print(link)
	link_id = re.split(r'/',str(link))
	#print(link_id[5])
user_id_list = table.find_all(get_user_id)
for user_id in user_id_list:
	if user_id.a is None:
		continue
	#print(user_id.a.string)
	#print(re.split(r'/',str(user_id.a['href']))[4])
remarks_num_list = table.find_all(get_remarks_list,text=re.compile("\d+"),class_='')
for remarks in remarks_num_list:
	print(remarks.string)
time_list =table.find_all('td',class_='time')
for time in time_list:
	print(time.string)
	
