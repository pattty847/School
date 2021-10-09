import json
from flask import Flask, request, abort
import tradeengine as kucoin

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
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
