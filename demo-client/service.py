from secrets import creds

import requests

url = "http://gunicorn:8000/"

r = requests.post(url + "rest-auth/login/", json={"username": creds["username"], "password": creds["password"]})
print(f"got response from kms on auth request: {r.text}")

set_cookie = r.headers['Set-Cookie']
csrf_token = set_cookie.split()[0].split("=")[1][:-1]
headers = {'X-CSRFToken': csrf_token, 'Cookie': set_cookie}
r = requests.get(url + "api/secret/GetSecret?key=my_best_key_2", headers=headers)
resp_json = r.json()['response']
print(f"got response from kms on get secret request: {resp_json}")
KEY = resp_json['key']
VALUE = resp_json['value']

r = requests.post('http://demo_server:9999/login', json={"key": KEY, "value": VALUE})

print(r.text)
