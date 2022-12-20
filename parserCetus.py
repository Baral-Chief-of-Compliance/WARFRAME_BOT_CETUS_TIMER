import requests
import json
import redis


def get_data_about_cetus():

    r = redis.Redis(host='localhost', port=6379, db=1)

    data_from_wf_hub = json.loads(r.get('WFHUB'))

    data_about_cetus = {}

    for key in data_from_wf_hub:
        if (key == "cetusCycle"):
            data_about_cetus = data_from_wf_hub[key]

    return data_about_cetus
