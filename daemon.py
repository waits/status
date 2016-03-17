#!/usr/local/bin/python3

import json, os, requests, time

with open('sites.json', 'w+') as file:
    file.close()

with open('config.json') as file:
    sites = json.load(file)['sites']
    file.close()

def check_status():
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
    with open('sites.json', 'w') as file:
        json.dump(sites, file)
        file.close()

while True:
    check_status()
    time.sleep(60)
