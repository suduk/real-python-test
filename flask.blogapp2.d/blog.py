from flask import Flask, redirect, url_for, session, g
from flask import request, render_template, flash
from functools import wraps
import sqlite3
app=Flask(__name__)
app.config.from_object('_config')

def required_login(f):
	@wraps(f)
	def wrapper(*args,**kwargs):
		if session.get('logged_in'):
			return f(*args,**kwargs)
		else:
			flash('You have to login')
			return redirect(url_for('login'))
	return wrapper

@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():
	if request.method=='POST':
		if request.form['login']!=app.config['LOGIN'] or request.form['password']!=app.config['PASSWORD']:
			flash('Wrong pass or username')
			#return redirect(url_for('login'))
			
		else:
			session['logged_in']=True
			flash('You are logged in')
			return redirect(url_for('main'))
	return render_template('login.html')

@app.route('/main')
@required_login
def main():
	g.db=sqlite3.connect(app.config['DATABASE'])
	cursor=g.db.cursor()
	x=cursor.execute('select * from blog').fetchall()	
	data_db=[dict(title=row[0],post=row[1]) for row in x]
	print data_db
	g.db.close()
	return render_template('main.html',data_db=data_db)

@app.route('/logout')
def logout():
	if session.get('logged_in'):
		session.pop('logged_in')
	print "DEBIG"
	return redirect(url_for('login'))


@app.route('/add',methods=['POST'])
def add():
	print request.form['title']
	print request.form['post']
	flash('You have added the post')
	return render_template('main.html')


if __name__=='__main__':
	app.run(debug=True)