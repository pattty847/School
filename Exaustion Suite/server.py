import json
from flask import Flask, request, abort
from flask.templating import render_template
from flask import Flask, request
from kucoin.client import Market
from kucoin.client import Trade
from kucoin.client import User

app = Flask(__name__)

# change

@app.route('/')
def welcome():
    return "welcome"

@app.route('/', methods=['POST'])
def webhook():

    # loads the requests data in json format
    data = json.loads(request.data)
    response = read_alert(data)

    # returns to webhook success or failer
    return {
        "code": "sucess",
        "message": response
    }

# API Information
# USDT ID: 61619d9942702600065eeb6d
api_key = "6161393bbc85c200065b0ca5"
api_secret = "bbe915da-6589-4187-92f5-a506de4b084b"
api_passphrase = "Apollo420$"

client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
user = User(api_key, api_secret, api_passphrase, is_sandbox=True)

# Stores the information in USDT wallet
balance = user.get_account("61619d9942702600065eeb6d")

# order_id = client.create_limit_order('BTC-USDT', 'buy', '1', '8000')

def limit_order(symbol, side, size, price):
    order = client.create_limit_order(symbol, side, size, price)

    return order

def read_alert(data):
    if(data['type'] == "market"):
        order = client.create_market_order(symbol=data['symbol'], side=data['side'], size=data['size'])
    elif(data['type'] == "limit"):
        order = client.create_limit_order(symbol=data['symbol'], side=data['side'], size=data['size'], price=data['price'])
    else:
        order = "Incorrect 'type' format. Please use 'market' or 'limit'."
    return client.get_order_details(order['orderId'])


if __name__ == "__main__":
    app.run()
