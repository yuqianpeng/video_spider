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


sql = """CREATE TABLE proxies(
					id int(10) unsigned NOT NULL AUTO_INCREMENT,
					ip varchar(15)  NOT NULL,
					port int(10) NOT NULL,
					htype varchar(15) NOT NULL ,
					PRIMARY KEY (id))"""

cursor.execute(sql)


db.close()