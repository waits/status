from flask import Flask
from flask import abort, redirect, render_template, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
