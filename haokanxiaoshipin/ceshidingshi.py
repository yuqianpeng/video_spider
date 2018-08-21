import time

def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec
second = sleeptime(0,0,5)
while 1==1:
	time.sleep(second)
	print('1111')
	# main('https://haokan.baidu.com/videoui/page/videoland?pd=haokan_share&context=%7B%22cuid%22%3A%220av6tjPW2i03iSuOga24i_uWSalli-fq_aH-ijanHaKWLMkRB%22%2C%22nid%22%3A%2212922407705409416517%22%7D')
