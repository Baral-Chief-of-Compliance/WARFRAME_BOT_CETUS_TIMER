import requests
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def get_data_about_arbitration():
    url = "https://api.warframestat.us/pc?language=ru"
    headers = {
        "Accept": "* / *",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    req = requests.get(url, headers)
    src = req.text

    data_from_wf_hub = json.loads(src)

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