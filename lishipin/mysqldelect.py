import pymysql
config = {
    'host': 'xxxxxx',
    'port': xxxx,
    'user': 'admin',
    'passwd': 'xxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}

db =pymysql.connect(**config)


cursor = db.cursor()

sql = "DELETE FROM yangcong_video_meipaigaoxiao WHERE id > 0 and id < 200 "
try:

   cursor.execute(sql)

   db.commit()
except:

   db.rollback()


db.close()