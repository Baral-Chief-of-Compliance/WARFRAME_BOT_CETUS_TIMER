import requests
import redis
import json


def get_date_from_wfhub():

    url = "https://api.warframestat.us/pc?language=ru"
    headers = {
        "Accept": "* / *",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    r = redis.Redis(host='localhost', port=6379, db=1)

    req = requests.get(url, headers)
    src = req.json()

    r.set('WFHUB', json.dumps(src))

