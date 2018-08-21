import socket
import pymysql
import requests
import random
from lxml import etree
from multiprocessing import Pool

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '111111',
    'db': 'ip_use',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()


user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", 
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", 
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", 
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def getipdaili():
  user_agent = random.choice(user_agent_list)
  headers = {'User-Agent':user_agent}
  for i in range(10,100):
    url = 'http://www.xicidaili.com/nn/' + str(i)
    r = requests.get(url=url, headers=headers)
    html_etree = etree.HTML(r.text)
    ip_list = html_etree.xpath('//table[@id="ip_list"]/tr')
    for i in range(1,len(ip_list)):
      ip = ip_list[i].xpath('./td/text()')[0]
      port = ip_list[i].xpath('./td/text()')[1]
      htype = ip_list[i].xpath('./td/text()')[5]

      if validateIp(ip,port,htype) is True:
        insertdb(ip,port,htype)

def validateIp(ip,port,htype):
  # print('begain')
  url = "http://ip.chinaz.com/getip.aspx"
  socket.setdefaulttimeout(3)
  try:
    # print(htype)
    proxy_temp = {repr(htype):ip + ":" + port}
    res = requests.get(url=url,proxies=proxy_temp)
    if (res.status_code == 200):
      print('验证成功')
      return True
  except Exception as e:
    print('验证失败')
    print(e)


def insertdb(ip,port,htype):
  try:
    sql0 = """SELECT id FROM proxies WHERE ip=(%s) and port=(%s) and htype=(%s)"""%(repr(ip),port,repr(htype))
    cursor.execute(sql0)
    result = cursor.fetchall()
    print('11111')
    if len(result) != 0 :
      print('数据库已经存在')

    else:
      sql1 = '''INSERT INTO proxies(ip,port,htype) VALUES(%s,%s,%s)'''%(repr(ip),port,repr(htype))
      cursor.execute(sql1)
      db.commit()
      print('ok')
  except Exception as e:
    print(e)
      


if __name__ == '__main__':
  getipdaili()
