from flask import Flask
app=Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello_world():
	return 'hello world'

@app.route('/hello/<name>/<int:age>')
def hello_name(name,age):
	return 'hello {}, {}'.format(name,age)

@app.route('/sciezka/<path:path_to_page>')
def hello_path(path_to_page):
	return 'hello {}'.format(path_to_page),200

if __name__=='__main__':
	app.run(debug=True)
#

