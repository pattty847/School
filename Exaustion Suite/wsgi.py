import json, config
from flask import Flask, request, abort
from flask.templating import render_template
from flask import Flask, request, redirect, url_for
from kucoin.client import Market, Trade, User
from pycoingecko import CoinGeckoAPI
from pprint import pprint

# Initialize our Flask application server
app = Flask(__name__)

# Initialize our CoinGeckoAPI
cg = CoinGeckoAPI()

# route() is a decorator which binds functions to URLs
# /index is the home page for the website
@app.route('/index')
def index():

    return render_template("index.html")

# /crypto displays the TradeSuite page
@app.route('/crypto')
def crypto():

    return render_template("crypto.html")

# this is a redirect to the index if the user goes to the root of the website
@app.route('/')
def redirectIndex():

    return redirect(url_for("index"))

# /webhook is where our Tradingview scripts will send json data
@app.route('/webhook', methods=['POST'])
def webhook():

    # loads the requests data in json format
    data = json.loads(request.data)

    # store the output of read_alert() which is our orderId
    response = read_alert(data)

    # returns to webhook success or failure and the orderId if successful
    return {
        "code": "sucess",
        "message": response
    }

# API Information
# USDT ID: 61619d9942702600065eeb6d
api_key = config.api_key
api_secret = config.api_secret
api_passphrase = config.api_passphrase

client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
user = User(api_key, api_secret, api_passphrase, is_sandbox=True)

# Stores the information in USDT wallet
balance = user.get_account("61619d9942702600065eeb6d")

# This list will store all of our previous orders so we can refer to them later
orders_list = []

# Function to place limit orders and add that order to the list of orders
def limit_order(symbol, side, size, price):
    price = int(float(price))
    order = client.create_limit_order(symbol, side, size, str(price))
    ladderTakeProfit(order)

    orders_list.append(client.get_order_details(order['orderId']))

    return order

# Function to place market orders and add that order to the list of orders
def market_order(symbol, side, size):
    order = client.create_market_order(symbol, side, size)

    orders_list.append(client.get_order_details(order['orderId']))

    return order

def ladderTakeProfit(orderId, chunks):
    entry = orderId['price']
    print(entry)

# Main read function that interprets webhook alerts
def read_alert(data):
    if(data['type'] == "market"):

        order = market_order(symbol=data['symbol'], side=data['side'], size=data['size'])

    elif(data['type'] == "limit"):

        order = limit_order(symbol=data['symbol'], side=data['side'], size=data['size'], price=data['price'])

    elif(data['type'] == "cancel"):
        
        order = client.cancel_all_orders()

    else:

        order = "Incorrect 'type' format. Please use 'market' or 'limit'."

    return order
    
def getTrendingCoins():
    return cg.get_search_trending()

def getCategories():
    return cg.get_coins_categories()

def coinLookup(name):
    return cg.get_coin_by_id(name, vs_currencies='usd')

if __name__ == "__main__":
    trending = getTrendingCoins()
    for coin in trending['coins']:
        pass
        # print(coin['item']['id'])

    categories = getCategories()
    for name in categories:
        pass
        # print(name['name'])


    print(coinLookup('bitcoin')['description'])