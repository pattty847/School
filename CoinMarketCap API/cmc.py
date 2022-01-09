# This example uses Python 2.7 and the python-request library.

from os import write
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
import numpy as numpy
import pandas as pd


api_key = ["31c20493-3635-494b-852a-904ffb636906"]

crypto_endpoints = {
    "categories": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories", 
    "category": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/category", 
    "metadata": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", 
    "cmc-id-map": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map", 
    "listing-latests": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", 
    "quotes": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
}

parameters = {
    'id': '1',
    'convert': 'usd'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '31c20493-3635-494b-852a-904ffb636906',
}

session = Session()
session.headers.update(headers)


def getData(endpoint, q_parameters):
    r = ""
    try:
        response = session.get(endpoint, params=q_parameters)
        r = json.loads(response.text)
        r = pd.DataFrame(r)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        r = e

    return r

print(getData(crypto_endpoints["quotes"], parameters).loc["1"])