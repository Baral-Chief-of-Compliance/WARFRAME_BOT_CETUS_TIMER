import requests
import redis
import json
import sched
import time
import daemon


update_schedule = sched.scheduler(time.time, time.sleep)
def get_date_from_wfhub():

    url = "https://api.warframestat.us/pc?language=ru"
    headers = {
        "Accept": "* / *",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    r = redis.Redis(host='localhost', port=6379, db=1)

    req = requests.get(url, headers)

    if req.status_code == 200:
        src = req.json()
        r.set('WFHUB', json.dumps(src))
        print('данные занесены в бд')

    else:
        print('какие-то проблемы')

    update_schedule.enter(180, 1, get_date_from_wfhub)


update_schedule.enter(180, 1, get_date_from_wfhub)


with daemon.DaemonContext():
    update_schedule.run()
