import re
import requests
from lxml import etree
import json
from selenium import webdriver
import time



def handle_video(name,video_url):
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
		r = requests.get(url=url1, headers=headers)
		filename = './video/' + name + '.mp4'
		try:
			with open(filename, 'wb') as fp:
				fp.write(r.content)
		except OSError:
			pass

def handle_data():
	path = r'C:\tool\chromedriver_win32\chromedriver.exe'

	driver = webdriver.Chrome(path)

	url = 'http://www.pearvideo.com/category_1'

	driver.get(url)
	time.sleep(2)


	for x in range(1, 3):
		load_button = driver.find_element_by_id('listLoadMore')
		load_button.click()
		
		time.sleep(2)


	html = driver.page_source
	# print(type(html))
	html_tree = etree.HTML(html)
	video_list = html_tree.xpath('//ul[@class="category-list clearfix"]/li[@class="categoryem"]/div[@class="vervideo-bd"]/a')
	# print(len(video_list))
	image_url = html_tree.xpath('//ul[@class="category-list clearfix"]/li[@class="categoryem"]/div[@class="vervideo-bd"]/a//div[@class="img"]/@style')
	for image in image_url:
		p0 = re.compile(r'(?<=[(])[^()]+\.[^()]+(?=[)])',re.S)
		image1 = p0.findall(image)
		print(image1)

	for video in video_list:

		video_url = video.xpath('./@href')

		name = video.xpath('./div[@class="vervideo-title"]/text()')
		# for name1 in name:
		# 	handle_video(name1,video_url)
	
	
if __name__ == '__main__':
	handle_data()
