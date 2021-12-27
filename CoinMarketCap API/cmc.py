# This example uses Python 2.7 and the python-request library.

from os import write
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

api_key = ["31c20493-3635-494b-852a-904ffb636906"]
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '31c20493-3635-494b-852a-904ffb636906',
}

session = Session()
session.headers.update(headers)


try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


