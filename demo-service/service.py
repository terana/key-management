from secrets import creds

import requests

url = "http://gunicorn:8000/"

r = requests.post(url + "rest-auth/login/", json={"username": creds["username"], "password": creds["password"]})

set_cookie = r.headers['Set-Cookie']
csrf_token = set_cookie.split()[0].split("=")[1][:-1]
headers = {'X-CSRFToken': csrf_token, 'Cookie': set_cookie}
r = requests.post(url + "api/", headers=headers)

print(r.text)
