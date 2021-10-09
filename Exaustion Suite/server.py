import json
from flask import Flask, request, abort
from flask.templating import render_template
import tradeengine as kucoin

app = Flask(__name__)

# change

@app.route('/')
def welcome():
    return "welcome"

@app.route('/', methods=['POST'])
def webhook():

    # loads the requests data in json format
    data = json.loads(request.data)
    response = kucoin.read_alert(data)

    # returns to webhook success or failer
    return {
        "code": "sucess",
        "message": response
    }


if __name__ == "__main__":
    app.run()
