import sqlite3

def create_db():
	#if you use with than you don't need connection.commit() and connection.close()
	with sqlite3.connect('new.db') as connection:
		connection
	#[first_name last_name company_name address city county 
	#state zip phone1 phone2 email web]

		cursor=connection.cursor()
		cursor.execute('drop table user')
		cursor.execute('''
						create table user(
							name text(25),lastname text(25),companyName text(55), 
							address text(55),city text(22),county text(5), state text(20),
							zip text(10), phone1 text(20), phone2 text(20),email text(200),
							web text(100) )			
					''')
		import csv
		values = csv.reader(open('sample500.csv', 'rU'))
		values.next()
		cursor.executemany('insert into user values(?,?,?,?,?,?,?,?,?,?,?,?)',values)
		#connection.commit()
		

with sqlite3.connect('new.db') as connection:
	cursor=connection.cursor()
	x=cursor.execute('''
					select * from user where name like 'J%'
				''')
data=x.fetchall()

with open('first_column.csv','a') as f:
	for record in data:
		f.write(record[0]+' '+record[1]+'\n')
	
def create_table2(x):
	with sqlite3.connect('new.db') as connection:
		cursor=connection.cursor()
		cursor.execute('''
							create table name_lastname(name text(25), lastname text(23))
			''')
		cursor.executemany('''
							insert into name_lastname values(?,?)
			''',x)
tab=[]
with open('first_column.csv','r') as f:
	first=False
	for name_lastname in f:
		if first:
			tup=(tuple(name_lastname.strip().split()))
			tab.append(tup)
		first=True
	print tab
create_table2(tab)
