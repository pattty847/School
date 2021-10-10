import json
from flask import Flask, request, abort
from flask.templating import render_template
from flask import Flask, request, redirect, url_for
from kucoin.client import Market, Trade, User

app = Flask(__name__)

# change

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/crypto')
def crypto():
    return render_template("crypto.html")

@app.route('/')
def redirectIndex():
    return redirect(url_for("index"))

@app.route('/webhook', methods=['POST'])
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
api_key = "6162fd36bc85c200065b10ea"
api_secret = "5815f4e7-d387-455a-8edb-d5b0a36320c0"
api_passphrase = "61619d9942702600065eeb6d"

client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
user = User(api_key, api_secret, api_passphrase, is_sandbox=True)

# Stores the information in USDT wallet
balance = user.get_account("61619d9942702600065eeb6d")

# order_id = client.create_limit_order('BTC-USDT', 'buy', '1', '8000')

def limit_order(symbol, side, size, price):
    order = client.create_limit_order(symbol, side, size, price)

    return order

def read_alert(data):
    price = int(float(data['price']))
    if(data['type'] == "market"):
        order = client.create_market_order(symbol=data['symbol'], side=data['side'], size=data['size'])
    elif(data['type'] == "limit"):
        order = client.create_limit_order(symbol=data['symbol'], side=data['side'], size=data['size'], price=str(price))
    elif(data['type'] == "cancel"):
        order = client.cancel_all_orders()
    else:
        order = "Incorrect 'type' format. Please use 'market' or 'limit'."
    return client.get_order_details(order['orderId'])


if __name__ == "__main__":
    app.run()
