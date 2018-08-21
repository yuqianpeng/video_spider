
import pymysql

from ippoxy import getipdaili


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

def getip():
	items = {}
	sql = """SELECT * FROM proxies """
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[1]
		port = row[2]
		htype = row[3]
		items['ip'] = ip
		items['port'] = port
		items['htype'] = htype
		return items

def removeip(ip,port,htype):
	cursor = db.cursor()
	sql = "DELETE FROM proxies WHERE ip=(%s) and port=(%s) and htype=(%s) " %(repr(ip),repr(port),repr(htype))
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	sql0 = """SELECT * FROM proxies """
	cursor.execute(sql0)
	results = cursor.fetchall()
	if len(results) <= 20:
		getipdaili()



