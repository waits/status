from flask import Flask
from flask import abort, redirect, render_template, url_for
import json
import requests

app = Flask(__name__)
with open('config.json') as file:
    app.config['SITES'] = json.load(file)['sites']
    file.close()

@app.route('/')
def root():
    sites = app.config['SITES']
    master_status = 'green'
    for site in sites:
        try:
            r = requests.get(site['url'], allow_redirects=False, timeout=5.0)
            if r.status_code >= 200 and r.status_code < 300:
                site['status'] = 'OK'
            else:
                site['status'] = r.status_code
                master_status = 'red'
        except requests.exceptions.ConnectionError:
            site['status'] = 'connection error'
            master_status = 'red'
        except requests.exceptions.Timeout:
            site['status'] = 'timeout'
            master_status = 'red'
    return render_template('index.html', sites=sites, master_status=master_status)

if __name__ == '__main__':
    app.debug = True
    app.run()
