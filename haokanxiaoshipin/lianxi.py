import base64
import random
import datetime
import re
import requests
import json
import time
import pymysql
import threading

from lxml import etree
from selenium import webdriver
from qiniu import Auth
from qiniu import BucketManager
from multiprocessing import Pool



count = 0


config = {
    'host': 'xxxxxxxxx',
    'port': xxxx,
    'user': 'admin',
    'passwd': 'xxxxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()




def qiniuyun(url,key):
	accessKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	secretKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	bucket  = 'xxxxx'
	q = Auth(accessKey, secretKey)
	bucketa = BucketManager(q)
	url1 = url
	key1 = key
	ret, info = bucketa.fetch(url1, bucket, key1)
	print('插入七牛云')
	assert ret['key'] == key



def handle_data(url):
	headers = {
	    'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
	    }
	try:
		r = requests.get(url=url, headers=headers)

		xhr = (r.text).encode('utf8')
		# print(type(r.text))
		html = etree.HTML(xhr)
		qian_title = html.xpath('//meta[@name="description"]/@content')
		if len(qian_title) == 0:
			title = ''
		else:
			title = qian_title[0]
		qian_video_url = html.xpath('//div[@class="player-container hide"]/video/@src')[0]
		video_url = qian_video_url.split('?')[0]
		# p = re.compile(r'"posterImage":".*?,"posterImageHistory""', re.S)
		# image_url = p.findall(r.text)
		qian_image_url = html.xpath('//div[@class="poster-background"]/@style')[0]
		p0 = re.compile(r'(?<=[(])[^()]+\.[^()]+(?=[)])',re.S)
		image = eval(p0.findall(qian_image_url)[0])
		image_url = re.sub(r'&amp;',"",image)
		print(title)
		print(video_url)
		print(image_url)
		handle_database(title,image_url,video_url)


		p1 = re.compile(r'"nid":"\d+"',re.S)
		vid_list = p1.findall(r.text)
		for qian_vid in vid_list:
			vid = eval(qian_vid.split(':')[1])
			handle_data('https://sv.baidu.com/sv?source=share-h5&pd=qm_share_mvideo&vid=' + vid)

	except Exception as e:
		print(e)





def handle_database(title,image_url,video_url):
	try:

		sql0 = """SELECT id FROM yangcong_caiji_haoxiao WHERE video_url = (%s)"""%(repr(video_url))
		cursor.execute(sql0)
		result = cursor.fetchall()
		if len(result) != 0 :
			print('数据库已经存在')
			return 

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

			uid = random.randint(1001, 88888)
			catid = 0
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

	except Exception as e:
		print(e)
		





def main():
	global count
	if count < 500:
		try:
			count += 1
			handle_data('https://sv.baidu.com/sv?source=share-h5&pd=qm_share_mvideo&vid=2090502311894018406')
	
		except Exception as e:
			print(e)
			main()
		finally:
			print('sucesse')


if __name__ == '__main__':
	main()
