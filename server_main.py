from flask import Flask, request, jsonify
from vsm import vsm, result_converter

app = Flask(__name__)

@app.route('/api/rating/', methods=['POST'])
def post_vsm_rating():
    vsm_result = vsm.run(request.json["query"], request.json["player"])
    estimated_result = result_converter.convert(vsm_result)
    vsm_result = max(vsm_result, key=vsm_result.get)
    response = jsonify({'estimated' : estimated_result, 'range' : vsm_result, 'player' : request.json["player"]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run()
