from flask import Flask
from flask import abort, redirect, render_template, url_for
from sassutils.wsgi import SassMiddleware
import json, requests, sched, threading, time

app = Flask(__name__)
app.debug = True
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'status': ('static/sass', 'static/css')
})

with open('config.json') as file:
    app.config['SITES'] = json.load(file)['sites']
    file.close()
@app.before_first_request
def start_worker_thread():
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# Runs check_status() every 60 seconds
def worker():
    check_status()
    exit_flag = threading.Event()
    while not exit_flag.wait(timeout=60):
        check_status()

# Makes a request to each site in the config and updates the global status dict
def check_status():
    sites = app.config['SITES'] # This may not be thread-safe
    for site in sites:
        print('Checking ' + site['url'])
        try:
            r = requests.get(site['url'], allow_redirects=False, timeout=5.0)
            if 200 <= r.status_code <= 299:
                site['status'] = ('ok', 'Online')
            elif 300 <= r.status_code <= 399:
                site['status'] = ('caution', 'Unexpected redirect')
            else:
                site['status'] = ('error', 'Reachable but returning errors'.format(r.status_code))
        except requests.exceptions.ConnectionError:
            site['status'] = ('error', 'Unreachable')
        except requests.exceptions.Timeout:
            site['status'] = ('error', 'Timeout')
        site['last_checked'] = time.time()

@app.route('/')
def root():
    master_status = 'ok'
    sites = list()
    for site in app.config['SITES']:
        if 'status' not in site: continue
        if site['status'][0] != 'ok': master_status = site['status'][0]
        t = time.strftime('%H:%M:%S', time.localtime(site['last_checked']))
        sites.append({'name': site['name'], 'status': site['status'], 'last_checked': t})
    return render_template('index.html', sites=sites, master_status=master_status)

if __name__ == '__main__':
    app.debug = True
    app.run()
