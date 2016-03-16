from flask import Flask
from flask import abort, redirect, render_template, url_for
import json
import requests

app = Flask(__name__)
with open('config.json') as file:
    app.config['SITES'] = json.load(file)['sites']
    file.close()

@app.route('/')
def hello_world():
    sites = app.config['SITES']
    for site in sites:
        try:
            r = requests.get(site['url'], allow_redirects=False, timeout=5.0)
            site['status'] = 'OK' if r.status_code >= 200 and r.status_code < 300 else r.status_code
        except requests.exceptions.ConnectionError:
            site['status'] = 'connection error'
        except requests.exceptions.Timeout:
            site['status'] = 'timeout'
    return render_template('index.html', sites=sites)

if __name__ == '__main__':
    app.debug = True
    app.run()
