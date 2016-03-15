from flask import Flask
from flask import abort, redirect, render_template, url_for
import json
import requests

app = Flask(__name__)
with open('config.json') as file:
    config = json.load(file)
    file.close()

@app.route('/')
def hello_world():
    sites = config['sites']
    for site in sites:
        try:
            r = requests.get(site['url'])
            site['status'] = r.status_code
        except requests.exceptions.ConnectionError:
            site['status'] = 0
    return render_template('index.html', sites=sites)

if __name__ == '__main__':
    app.debug = True
    app.run()
