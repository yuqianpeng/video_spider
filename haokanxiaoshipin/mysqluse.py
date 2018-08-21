import pymysql


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

def mselect(releation_url):
	sql = '''SELECT id FROM releation WHERE releation_url=(%s)''' % (releation_url)
	cursor.execute(sql)
	results = cursor.fetchall()
	return len(results)

def m1select():
	sql = '''SELECT releation_url FROM releation'''
	cursor.execute(sql)
	results = cursor.fetchall()
	return results

def minsert(releation_url):
	sql = """INSERT INTO releation(releation_url) VALUES (%s)""" %(releation_url)
	try:
	   cursor.execute(sql)
	   db.commit()
	except:
	   db.rollback()