from flask import Flask, jsonify, request, abort
from pathlib import Path
import yaml
from argparse import ArgumentParser

request_index = 0
mock_requests = []
app = Flask(__name__)
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/api/<path:path>', methods=HTTP_METHODS)
def catch_all(path):
    global request_index
    if request_index >= len(mock_requests):
        abort(500)

    curr_mock = mock_requests[request_index]
    if request.path != curr_mock['route']:
        abort(500)

    if request.method != curr_mock['method']:
        abort(500)

    if request.method == 'POST' and request.get_json(silent=True) != curr_mock['body_params']:
        abort(500)

    request_index += 1
    return jsonify(curr_mock['response_body']), curr_mock['response_code']

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-s", "--scenario")

    args = parser.parse_args()
    
    scenario_path = Path().resolve().parent / 'mocks' / f'{args.scenario}.yaml'
    with scenario_path.open() as f:
        mock_requests = yaml.safe_load(f)

    app.run(debug=True)
