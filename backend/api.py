from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/api/basic', methods=['GET'])
def basic_get():
    return jsonify({'basic': 'get'})

@app.route('/api/basic', methods=['POST'])
def basic_post():
    return jsonify({'basic': 'post'})

@app.route('/api/param/<param>', methods=['GET'])
def path_param(param):
    return jsonify({'get_param': param})

@app.route('/api/param', methods=['POST'])
def body_param():
    data = request.get_json()
    return jsonify({'post_param': data['param']})

if __name__ == '__main__':
    app.run(debug=True)
