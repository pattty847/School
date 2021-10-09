import time
import json
from flask import Flask, request
import requests
import hmac
import hashlib
import base64


api_key = "6161393bbc85c200065b0ca5"
api_secret = "bbe915da-6589-4187-92f5-a506de4b084b"
api_passphrase = "Apollo420$"
url = 'https://openapi-sandbox.kucoin.com/api/v1/accounts'
now = int(time.time() * 1000)
str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
signature = base64.b64encode(
    hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
passphrase = base64.b64encode(hmac.new(api_secret.encode(
    'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
headers = {
    "KC-API-SIGN": signature,
    "KC-API-TIMESTAMP": str(now),
    "KC-API-KEY": api_key,
    "KC-API-PASSPHRASE": passphrase,
    "KC-API-KEY-VERSION": "2"
}
response = requests.request('get', url, headers=headers)
print(response.status_code)
print(response.json())
