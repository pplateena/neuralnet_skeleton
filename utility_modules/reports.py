import os

import requests
import json

def send_request(message=None, image=None, status=None, additional_info=None):
    with open('personal_cache/maintainer_creds.txt', 'r') as file:
        lines = file.readlines()
        pc_id, worker_id, request_url = lines[0].strip(), lines[1].strip(), lines[2].strip() + '/receive_data'
        print (pc_id, worker_id, request_url)

    data = {
        "sender": {
            "PC_ID": pc_id,
            "Worker_ID": worker_id
        },
        "message": message
    }
    if message:
        data['message'] = message
    if status:
        data["status"] = status
    if additional_info:
        data["additional_info"] = additional_info

    data_json = json.dumps(data)
    files = {}

    if image:
        files["image"] = open('screenshot.png', "rb")


    if data:
        files["data"] = (None, data_json)  # Add image as a file object

    print('sending request')
    response = requests.post(request_url, files=files)

