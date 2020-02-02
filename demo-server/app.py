import logging
from secrets import creds

import requests
from flask import Flask, request

app = Flask('stock_pricer')

kms_url = "http://gunicorn:8000/"

r = requests.post(kms_url + "rest-auth/login/", json={"username": creds["username"], "password": creds["password"]})
print(f"got response from kms on auth request: {r.text}")

set_cookie = r.headers['Set-Cookie']
csrf_token = set_cookie.split()[0].split("=")[1][:-1]
headers = {'X-CSRFToken': csrf_token, 'Cookie': set_cookie}

r = requests.get(kms_url + "api/secret/GetSecret?key=my_best_key_2", headers=headers)
resp_json = r.json()['response']
print(f"got response from kms on get secret request: {resp_json}")
KEY = resp_json['key']
VALUE = resp_json['value']


@app.route('/login', methods=['POST'])
def login():
    key = request.json['key']
    value = request.json['value']

    logging.critical(f"asked for login: key={key}, value={value}; actual are {KEY}, {VALUE}")

    if key == KEY and value == VALUE:
        return "SUCCESS"

    return "The wrong secret."


app.run("0.0.0.0", "9999")
