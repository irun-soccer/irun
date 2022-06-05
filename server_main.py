from flask import Flask, request
from vsm import vsm

app = Flask(__name__)

@app.route('/api/rating/', methods=['POST'])
def post_vsm_rating():
    result = vsm.run(request.json["query"], request.json["player"])
    return result


if __name__ == '__main__':
    app.run()