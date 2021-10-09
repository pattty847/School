import json
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    print(data)

    return {
        "code": "sucess",
        "message": data
    }

if __name__ == "__main__":
    app.run()