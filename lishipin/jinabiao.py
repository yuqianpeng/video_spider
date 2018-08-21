

import pymysql


config = {
    'host': 'xxxxxxxxxxxxxxx',
    'port': xxxx,
    'user': 'admin',
    'passwd': 'xxxxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}
db =pymysql.connect(**config)


cursor = db.cursor()


sql = """CREATE TABLE yangcong_video_lishipinheng(
					id int(10) unsigned NOT NULL AUTO_INCREMENT,
					uid int(10) unsigned NOT NULL DEFAULT '0' ,
					catid smallint(5) unsigned NOT NULL DEFAULT '0' ,
					title char(120) NOT NULL DEFAULT '',
					thumb char(120) NOT NULL DEFAULT '',
					keywords char(120) NOT NULL DEFAULT '' ,
					video char(120) NOT NULL DEFAULT '' ,
					duration smallint(5) unsigned NOT NULL DEFAULT '0' ,
					size char(6) NOT NULL DEFAULT '0.00',
					width smallint(5) unsigned NOT NULL DEFAULT '0',
					height smallint(5) unsigned NOT NULL DEFAULT '0',
					createtime int(10) unsigned NOT NULL DEFAULT '0',
					PRIMARY KEY (id))"""

cursor.execute(sql)


db.close()