import requests
from requests.auth import HTTPBasicAuth
import json

CLIENT_ID = 'bGx7g2Oogzhs3hq2pb2tBg'
SECRET_KEY = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

with open('PASSWORD.txt', 'r') as f:
    pw = f.read()

data = {
    'grant_type': 'password',
    'username': 'tester78780',
    'password': pw
}

headers = {'User-Agent': 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
    auth = auth, data = data, headers = headers)

TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization' : f'bearer {TOKEN}'}}
# convert response to JSON and pull access_token value

print(requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json())