import requests
import json
import redis
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def get_data_about_arbitration():

    r = redis.Redis(host='localhost', port=6379, db=1)

    data_from_wf_hub = json.loads(r.get('WFHUB'))

    data_about_arbitration = {}

    procesed_data = {}

    for key in data_from_wf_hub:
        if (key == "arbitration"):
            data_about_arbitration = data_from_wf_hub[key]

    for key in data_about_arbitration:
        if (key == 'expiry'):
            expiry = datetime.strptime(data_about_arbitration[key], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('Europe/Moscow'))
            left = expiry - datetime.now(timezone.utc)
            procesed_data['left_time'] = left.seconds %3600//60

        if (key == 'type'):
            procesed_data['type'] = data_about_arbitration[key]

        if (key == 'enemy'):
            procesed_data['enemy'] = data_about_arbitration[key]

        if (key == 'node'):
            procesed_data['node'] = data_about_arbitration[key]

    return procesed_data

# print(get_data_about_cetus())


print(get_data_about_arbitration())