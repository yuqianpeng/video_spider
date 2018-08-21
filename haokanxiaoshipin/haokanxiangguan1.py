
import base64
import random
import datetime
import re
import requests
import json
import time
import pymysql

from lxml import etree
from selenium import webdriver
from qiniu import Auth
from qiniu import BucketManager
from multiprocessing import Pool

from mysqluse import mselect,minsert,m1select
from useip import getip,removeip

releation_list1 = []



config = {
    'host': 'xxxxxxxxxxx',
    'port': xxxxx,
    'user': 'admin',
    'passwd': 'xxxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()




def qiniuyun(url,key):
	accessKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	secretKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	bucket  = 'xxxxxx'
	q = Auth(accessKey, secretKey)
	bucketa = BucketManager(q)
	url1 = url
	key1 = key
	ret, info = bucketa.fetch(url1, bucket, key1)
	print('插入七牛云')
	assert ret['key'] == key

def handle_mysql(title,image_url,video_url):

	sql0 = """SELECT id FROM yangcong_caiji_haoxiao WHERE title = (%s)"""%(repr(title))
	cursor.execute(sql0)
	result = cursor.fetchall()
	if len(result) != 0 :
		print('数据库已经存在')
		pass
	else:

		sql1 = '''INSERT INTO yangcong_caiji_haoxiao(title,image_url,video_url) VALUES(%s,%s,%s)'''%(repr(title),repr(image_url),repr(video_url))
		cursor.execute(sql1)
		db.commit()
		str1 = random.sample('abcdefghijklmnopqrstuvwxyz0123456789',9)
		str2 = ""
		for i in str1:
		    str2 = str2 + i
		key = datetime.datetime.now().strftime('%Y/%m%d/%H%M%S') + str2
		imagekey = key + '.jpg'
		videokey = key + '.mp4'
		qiniuyun(image_url, imagekey)
		qiniuyun(video_url, videokey)

		uid = random.randint(1001, 88887)
		catid = 2
		title = title
		keywords = title
		# width = 
		# height = 
		duration = 0
		size = 0
		createtime = time.time()

		thumb = 'http://imgcdn.yangcongv.com/' + imagekey
		video ='http://v.yangcongv.com/' + videokey

		sql = """INSERT INTO yangcong_video_haoxiao(uid,catid,title,keywords,duration,size,createtime,thumb,video) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""%(uid,catid,repr(title),repr(keywords),duration,size,createtime,repr(thumb),repr(video))
		cursor.execute(sql)
		db.commit()
		print('插入数据库')	

def handle_releation():
	global releation_list1
	# print(releation_list1)
	for i in range(len(releation_list1)):
		url = releation_list1.pop(0)
		handle_data('https://haokan.baidu.com' + url)

def handle_data(url):
	global releation_list1
	if len(releation_list1) > 30000:
		releation_list1 = releation_list1[0:30001]
	items = getip()
	ip = items['ip']
	port = items['port']
	htype = items['htype']
	temp_ip = {repr(htype):repr(ip) + ":" + repr(port)}
	print(temp_ip)
	headers = {
	    'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
	    }
	r = requests.get(url=url, headers=headers, proxies=temp_ip)
	if r.status_code == 200:
		html_etree = etree.HTML(r.text)
		# print(html_etree)
		a_list = html_etree.xpath('//a')
		# print(a_list)
		releation_list = html_etree.xpath('//a/@href')
		for releations in releation_list:
			if releations not in releation_list1:
				releation_list1.append(releations)
			else:
				print('相关url已经存在了')
		# print(releation_list)
		for a in a_list:
			try:
				releation = a.xpath('./@href')[0]
				title = a.xpath('./@data-title')[0]
				image_url = a.xpath('./div[@class="c-blocka c-span4"]/div[@class="c-img c-img-y"]/img/@src')[0]
				qian_video_url = a.xpath('./@data-playurl')[0]
				video_url = qian_video_url.split('?')[0]
				print(releation)
				print(title)
				print(image_url)
				print(video_url)
				handle_mysql(title,image_url,video_url)
			except Exception as e:
				print(e)
				continue
		handle_releation()

	else:
		removeip(ip,port,htype)
		handle_data(json_url)

def main(url):
	handle_data(url)


if __name__ == '__main__':
	count = 0
	def sleeptime(hour,min,sec):
		return hour*3600 + min*60 + sec
	second = sleeptime(6,0,0)
	while 1==1:
		try:

			if count < 10:
				try:
					count += 1
					p = Pool(4)
					for i in range(4):
					    p.apply_async(main('https://haokan.baidu.com/videoui/page/videoland?pd=haokan_share&context=%7B%22cuid%22%3A%220av6tjPW2i03iSuOga24i_uWSalli-fq_aH-ijanHaKWLUGqB%22%2C%22nid%22%3A%228220389383368449882%22%7D'))
					    p.close()
					    p.join() 
				except Exception as e:
					print(e)
					p = Pool(4)
					for i in range(4):
					    p.apply_async(main('https://haokan.baidu.com/videoui/page/videoland?pd=haokan_share&context=%7B%22cuid%22%3A%220av6tjPW2i03iSuOga24i_uWSalli-fq_aH-ijanHaKWLUGqB%22%2C%22nid%22%3A%228220389383368449882%22%7D'))
					    p.close()
					    p.join()
		except Exception as e:
			print(e)
			continue

# https://haokan.baidu.com/videoui/page/videoland?pd=haokan_share&context=%7B%22cuid%22%3A%220av6tjPW2i03iSuOga24i_uWSalli-fq_aH-ijanHaKWLMkRB%22%2C%22nid%22%3A%229547993663197236619%22%7D 美食
		
		time.sleep(second)


# if __name__ == '__main__':
# 	p = Pool(4)
# 	for i in range(4):
# 		p.apply_async(main)
# 	p.close()
# 	p.join()

