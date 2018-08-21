import pymysql
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

sql = """SELECT id FROM yangcong_video_chigua WHERE title=(%s)"""%(repr("大碰牛"))

cursor.execute(sql)
result = cursor.fetchall()
print(result)
