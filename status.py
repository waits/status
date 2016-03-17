from flask import Flask
from flask import abort, redirect, render_template, url_for
import json, requests, threading, time

app = Flask(__name__)
with open('config.json') as file:
    app.config['SITES'] = json.load(file)['sites']
    file.close()

@app.before_first_request
def start_worker_thread():
    t = threading.Thread(target=check_status, daemon=True)
    t.start()
    print(t.name)

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

def check_status():
    sites = app.config['SITES'] # This may not be thread-safe
    while True:
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
        time.sleep(15) # Replace this with a sched.scheduler

if __name__ == '__main__':
    app.debug = True
    app.run()
