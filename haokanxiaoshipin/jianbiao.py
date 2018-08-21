import pymysql


config = {
    'host': 'xxxxx',
    'port': xxxx,
    'user': 'admin',
    'passwd': 'xxxxxxxx',
    'db': 'xxxxx',
    'charset': 'utf8'
}
db =pymysql.connect(**config)

cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 创建数据表SQL语句
sql = """CREATE TABLE releation(
			id int(10) auto_increment,
			releation_url varchar(255) NOT NULL,
			PRIMARY KEY (id))"""

cursor.execute(sql)

# 关闭数据库连接
db.close()