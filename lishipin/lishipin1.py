
import random
import datetime
import re
import requests
from lxml import etree
import json
from selenium import webdriver
import time
import pymysql

from qiniu import Auth
from qiniu import BucketManager

config = {
    'host': 'x',
    'port': 8866,
    'user': 'admin',
    'passwd': 'x',
    'db': 'x',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()



def qiniuyun(url,key):
	accessKey = 'x'
	secretKey = 'x'
	bucket  = 'x'
	q = Auth(accessKey, secretKey)
	bucketa = BucketManager(q)
	url1 = url
	key1 = key
	ret, info = bucketa.fetch(url1, bucket, key1)
	print('插入七牛云')
	assert ret['key'] == key

def handle_video(video_url):
	headers = {
		'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
	}
	for video in video_url:
	    video_url1 = 'http://www.pearvideo.com/' + video
	r = requests.get(url=video_url1, headers=headers)

	p = re.compile(r'srcUrl=".*.mp4"',re.S)
	url = p.findall(r.text)
	for i in url:
		url1 = (eval(i.split('=')[1]))
		return url1

def handle_image(image_url):
	for image in image_url:
		p0 = re.compile(r'(?<=[(])[^()]+\.[^()]+(?=[)])',re.S)
		image1 = p0.findall(image)
	for img in image1:
		return img

def handle_name(name):
    for na in name:
    	return na

def handle_data(url,catid):
	path = r'C:\tool\chromedriver_win32\chromedriver.exe'

	driver = webdriver.Chrome(path)

	url = url

	driver.get(url)
	time.sleep(3)


	for x in range(1, 85):
		load_button = driver.find_element_by_id('listLoadMore')
		load_button.click()
		
		time.sleep(2)


	html = driver.page_source
	# print(type(html))
	html_tree = etree.HTML(html)
	video_list = html_tree.xpath('//ul[@class="category-list clearfix"]/li[@class="categoryem"]/div[@class="vervideo-bd"]/a')

	for video in video_list:

		try:

			video_url = video.xpath('./@href')
			video_url1 = handle_video(video_url)
			print(video_url1)
			image_url = video.xpath('./div[@class="vervideo-img"]/div[@class="verimg-view"]/div[@class="img"]/@style')
			image1 = handle_image(image_url)

			print(image1)


			name = video.xpath('./div[@class="vervideo-title"]/text()')
			name1 = handle_name(name)
			print(name1)
			# return name1,image1,video_url1
			sql0 = """SELECT id FROM yangcong_caiji_lishipin WHERE video_url = (%s)"""%(repr(video_url1))
			cursor.execute(sql0)
			result = cursor.fetchall()
			if len(result) != 0 :
				print('数据库已经存在')
				continue
			else:

				sql1 = '''INSERT INTO yangcong_caiji_lishipin(title,image_url,video_url) VALUES(%s,%s,%s)'''%(repr(name1),repr(image1),repr(video_url1))
				cursor.execute(sql1)
				db.commit()
				str1 = random.sample('abcdefghijklmnopqrstuvwxyz0123456789',9)
				str2 = ""
				for i in str1:
				    str2 = str2 + i
				key = datetime.datetime.now().strftime('%Y/%m%d/%H%M%S') + str2
				imagekey = key + '.jpg'
				videokey = key + '.mp4'
				qiniuyun(image1, imagekey)
				qiniuyun(video_url1, videokey)

				uid = random.randint(1001, 88887)
				catid = catid
				title = name1
				keywords = name1
				# width = 
				# height = 
				duration = 0
				size = 0
				createtime = time.time()

				thumb = 'http://imgcdn.yangcongv.com/' + imagekey
				video ='http://v.yangcongv.com/' + videokey

				sql = """INSERT INTO yangcong_video_lishipinheng(uid,catid,title,keywords,duration,size,createtime,thumb,video) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""%(uid,catid,repr(title),repr(keywords),duration,size,createtime,repr(thumb),repr(video))
				cursor.execute(sql)
				db.commit()
				print('插入数据库')
		except Exception as e:
			print(e)
			continue

	driver.quit()



if __name__ == '__main__':

	mediauau = [
	            ('http://www.pearvideo.com/author_11549088',13),
	            ('http://www.pearvideo.com/author_11549090',13),
	            ('http://www.pearvideo.com/author_11549111',13),
	            ('http://www.pearvideo.com/author_11539934',13),
	            ('http://www.pearvideo.com/author_11742488',13),
	            ('http://www.pearvideo.com/author_11869415',13),
	            ('http://www.pearvideo.com/author_11504225',13),
	            ('http://www.pearvideo.com/author_10140198',13),
	            ('http://www.pearvideo.com/author_10053415',13),
	            ('http://www.pearvideo.com/author_11900907',13),
                ('http://www.pearvideo.com/author_11367470',13),
                ('http://www.pearvideo.com/author_11278322',13),
                ('http://www.pearvideo.com/author_10696291',21),
                ('http://www.pearvideo.com/author_11881540',16),
                ('http://www.pearvideo.com/author_10947850',16)
	            ]

	for url,catid in mediauau:
		handle_data(url,catid)
		print('一个对应标签网站爬完')
		time.sleep(10)
		print('睡了10s继续干活')

