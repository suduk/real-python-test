import sqlite3 
db_data=[("title1", "some post 1"),("title2","some post2...")]
with sqlite3.connect("blog.db") as connection:
	cursor=connection.cursor()
	cursor.execute('drop table blog')
	cursor.execute('create table blog(title text, post text)')
	cursor.executemany('insert into blog values(?,?)',db_data)
