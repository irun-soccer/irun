from flask import Flask, request, jsonify
from vsm import vsm

app = Flask(__name__)

@app.route('/api/rating/', methods=['POST'])
def post_vsm_rating():
    vsm_result = vsm.run(request.json["query"], request.json["player"])
    response = jsonify({'rating' : vsm_result, 'player' : request.json["player"]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run()
