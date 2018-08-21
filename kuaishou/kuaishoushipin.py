
import base64
import random
import datetime
import re
import requests
import json
import time
import pymysql
import sys
import io

from lxml import etree
from selenium import webdriver
from qiniu import Auth
from qiniu import BucketManager

from useip import getip,removeip

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
count = 0
config = {
    'host': 'xxxxxxxxxxxx',
    'port': xxxx,
    'user': 'xxxxx',
    'passwd': 'xxxxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()


def qiniuyun(url,key):
	accessKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	secretKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	bucket  = 'onion'
	q = Auth(accessKey, secretKey)
	bucketa = BucketManager(q)
	url1 = url
	key1 = key
	ret, info = bucketa.fetch(url1, bucket, key1)
	print('插入七牛云')
	assert ret['key'] == key


def handle_data(json_url):
	items = getip()
	ip = items['ip']
	port = items['port']
	htype = items['htype']
	temp_ip = {repr(htype):repr(ip) + ":" + repr(port)}
	print(temp_ip)
	headers = {
	'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'}
	try:
		r = requests.get(url=json_url, headers=headers, proxies=temp_ip)
		print("代理ip运行了")
		html = (r.text).encode('utf8')
		ss = str(html,encoding='utf8')

		obj = json.loads(ss)
		# print(obj)
		for video_obj in obj['feeds']:
			# title = eval(video_obj['caption'])
			try:
				title = str(video_obj['caption'])
				image_url = ''
				qian_video_url = video_obj['main_mv_urls'][0]['url']
				video_url = qian_video_url.split('?')[0]
				# print(title)
				print(image_url)
				print(video_url)


		# p0 = re.compile(r'"caption":".*?"', re.S)
		# qian_title = p0.findall(ss)
		# p1 = re.compile(r'"headurls":.*?,"url":".*?"', re.S)
		# qian_image_url = p1.findall(ss)
		# p2 = re.compile(r'"main_mv_urls":.*?,"url":".*?"', re.S)
		# qian_video_url = p2.findall(ss)
		# print(len(qian_title))
		# print(len(qian_image_url))
		# print(len(qian_video_url))



				sql0 = """SELECT id FROM yangcong_caiji_chigua WHERE video_url = (%s)"""%(repr(video_url))
				cursor.execute(sql0)
				result = cursor.fetchall()
				if len(result) != 0 :
					print('数据库已经存在')
					continue
				else:

					sql1 = '''INSERT INTO yangcong_caiji_chigua(title,video_url) VALUES(%s,%s)'''%(repr(title),repr(video_url))
					cursor.execute(sql1)
					db.commit()
					str1 = random.sample('abcdefghijklmnopqrstuvwxyz0123456789',9)
					str2 = ""
					for i in str1:
					    str2 = str2 + i
					key = datetime.datetime.now().strftime('%Y/%m%d/%H%M%S') + str2
					# imagekey = key + '.jpg'
					videokey = key + '.mp4'
					# qiniuyun(image_url, imagekey)
					qiniuyun(video_url, videokey)

					uid = random.randint(1001, 88887)
					catid = 0
					title = title
					keywords = title
					# width = 
					# height = 
					duration = 0
					size = 0
					createtime = time.time()

					# thumb = 'http://imgcdn.yangcongv.com/' + imagekey
					thumb = ''
					video ='http://v.yangcongv.com/' + videokey

					sql = """INSERT INTO yangcong_video_chigua(uid,catid,title,keywords,duration,size,createtime,thumb,video) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""%(uid,catid,repr(title),repr(keywords),duration,size,createtime,repr(thumb),repr(video))
					cursor.execute(sql)
					db.commit()
					print('插入数据库')

			except Exception as e:
				print(e)
				continue
	except Exception as e:
		print(e)
		removeip(ip,port,htype)
		handle_data(json_url)




def main():
	global count
	if count < 500:
		try:
			count += 1
			list1 = ['type=7&page=3&coldStart=false&count=20&pv=false&id=92&refreshTimes=2&pcursor=1&source=1&extInfo=K8xa%2FeUMjPbPkuqZb%2F7Y2YuXQqjy07aij7GfjYtKy34%3D&__NStokensig=8c6ef61743f3f448a0453fa1c10c73fa77202ed790e2ff9d6b4059c249417b18&token=e2803b8090ff42c6b06b1de7675f9df3-198192687&client_key=3c2cd3f3&os=android&sig=7a9ae899d7063af9c7b955a0925347bc']
			for i in range(10000):
				for uid in list1:
					url = 'http://api.ksapisrv.com/rest/n/feed/hot?mod=HUAWEI%28SLA-AL00%29&lon=116.441866&country_code=cn&did=ANDROID_206c7dcb1363d0f6&app=0&net=WIFI&oc=UNKNOWN&ud=198192687&c=HUAWEI&sys=ANDROID_7.0&appver=5.7.4.6246&ftt=&language=zh-cn&iuid=DuA88LW8fvp3DIkKnBgsZklXkD0ToPxlm4CNBgZlJqK2QnfAALtDb1HwKHG9trlaGu4uhWRERKDDLmZVirtpdfcg&lat=39.955057&did_gt=1527134714310&ver=5.7&max_memory=384&' + uid
					# print(url)
					handle_data(url)
					time.sleep(2)
	
		except Exception as e:
			print(e)
			main()
		finally:
			print('sucesse')






	
if __name__ == '__main__':
	main()

