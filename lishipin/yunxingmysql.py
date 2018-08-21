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
    'port': x,
    'user': 'x',
    'passwd': 'x',
    'db': 'x',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()


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

def handle_data():
	path = r'C:\tool\chromedriver_win32\chromedriver.exe'

	driver = webdriver.Chrome(path)

	url = 'http://www.pearvideo.com/category_1'

	driver.get(url)
	time.sleep(2)


	for x in range(1, 2):
		load_button = driver.find_element_by_id('listLoadMore')
		load_button.click()
		
		time.sleep(2)


	html = driver.page_source
	# print(type(html))
	html_tree = etree.HTML(html)
	video_list = html_tree.xpath('//ul[@class="category-list clearfix"]/li[@class="categoryem"]/div[@class="vervideo-bd"]/a')

	for video in video_list:

		video_url = video.xpath('./@href')
		video_url1 = handle_video(video_url)
		print(video_url1)
		image_url = video.xpath('./div[@class="vervideo-img"]/div[@class="verimg-view"]/div[@class="img"]/@style')
		image1 = handle_image(image_url)
		# print(type(image1))
		name = video.xpath('./div[@class="vervideo-title"]/text()')
		name1 = handle_name(name)
		# print(image1)
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
			uid = random.randint(1001, 88888)
			catid = 2
			title = name1
			keywords = name1
			# width = 
			# height = 
			duration = 0
			size = 0
			createtime = time.time()
			thumb = image1
			video = video_url1
			sql = """INSERT INTO yangcong_video_lishipin(uid,catid,title,keywords,duration,size,createtime,thumb,video) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""%(uid,catid,repr(title),repr(keywords),duration,size,createtime,repr(thumb),repr(video))
			cursor.execute(sql)
			db.commit()

if __name__ == '__main__':
	handle_data()