from flask import Flask
from flask import abort, redirect, render_template, url_for
import json, subprocess, time

app = Flask(__name__)

@app.route('/')
def root():
    if __name__ == '__main__':
        with open('sites.json') as file:
            sites = json.load(file)
            file.close()
    else:
        sites = app.config['SITES']
    master_status = 'green'
    for site in sites:
        if site['status'] != 'OK': master_status = 'red'
        t = time.localtime(site['last_checked'])
        site['last_checked'] = time.strftime('%H:%M:%S', t)
    return render_template('index.html', sites=sites, master_status=master_status)

if __name__ == '__main__':
    process = subprocess.Popen('./daemon.py')
    app.debug = True
    app.run()
