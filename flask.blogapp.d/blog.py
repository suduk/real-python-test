from flask import Flask, render_template, request, session, url_for, redirect, flash, g
from functools import wraps
import sqlite3

app=Flask(__name__)
app.config.from_object('config')
def connect_db():
	print app.config['DATABASE']
	return sqlite3.connect(app.config['DATABASE'])


@app.route('/',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['login']!=app.config['USERNAME'] or request.form['password']!=app.config['PASSWORD']:
			error='Wrong pass or login'
		else:

			session['logged_in']=True
			return redirect(url_for('main'))
	return render_template('login.html',error=error)


def login_required(f):
  	@wraps(f)
	def wrapper(*args,**kwargs):
		#if session['logged_in']:
		if session.get('logged_in'):
			return f(*args,**kwargs)
		else:
			flash('you need to login first motherfucker')
			return redirect(url_for('login'))
	return wrapper


@app.route('/main')
@login_required
def main():
	g.db=connect_db()
	cursor=g.db.cursor()
	cursor.execute('select * from posts')
	#print cursor.fetchall()
	posts=[dict(title=row[0],post=row[1]) for row in cursor.fetchall()]
	#posts=[dict(title=row[0],post=row[1]) for row in cursor.fetchall()]
	g.db.close()
	print posts
	return render_template('main.html',posts=posts)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')

	return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add():
	print "inside f add()"
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into posts (title, post) values (?,?)',[request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))

if __name__=='__main__':
	print app.config['DATABASE']
	app.run(debug=True)



