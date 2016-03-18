from flask import Flask
from flask import abort, redirect, render_template, url_for
import json, requests, sched, threading, time
app = Flask(__name__)

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
            if r.status_code >= 200 and r.status_code < 300:
                site['status'] = 'OK'
            else:
                site['status'] = r.status_code
        except requests.exceptions.ConnectionError:
            site['status'] = 'connection error'
        except requests.exceptions.Timeout:
            site['status'] = 'timeout'
        site['last_checked'] = time.time()

@app.route('/')
def root():
    master_status = 'green'
    sites = list()
    for site in app.config['SITES']:
        if 'status' not in site: continue
        if site['status'] != 'OK': master_status = 'red'
        t = time.strftime('%H:%M:%S', time.localtime(site['last_checked']))
        sites.append({'name': site['name'], 'status': site['status'], 'last_checked': t})
    return render_template('index.html', sites=sites, master_status=master_status)

if __name__ == '__main__':
    with open('config.json') as file:
        app.config['SITES'] = json.load(file)['sites']
        file.close()

    @app.before_first_request
    def start_worker_thread():
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    app.debug = True
    app.run()
