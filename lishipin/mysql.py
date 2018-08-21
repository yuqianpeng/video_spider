import pymysql
config = {
    'host': 'xxxx',
    'port': xxxx,
    'user': 'admin',
    'passwd': 'xxxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()

sql = '''rename table yangcong_caiji_lishipin to yangcong_video_lishipin'''

cursor.execute(sql)


result = cursor.fetchone()
print(result)