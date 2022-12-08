import requests
import json


def get_data_about_cetus():
    url = "https://api.warframestat.us/pc?language=ru"
    headers = {
        "Accept": "* / *",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    req = requests.get(url, headers)
    src = req.text

    data_from_wf_hub = json.loads(src)

    for key in data_from_wf_hub:
        if (key == "cetusCycle"):
            data_about_cetus = data_from_wf_hub[key]

    return data_about_cetus

