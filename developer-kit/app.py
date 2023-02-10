from flask import Flask, request, jsonify
import logging
from telco import Telco
import json

# Configure application
app = Flask(__name__)
telco_ = Telco()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

@app.route('/')
def index():
    return 'Welcome to the Developer Kit!', 200

@app.route('/purposes', methods=['POST'])
def create_purpose():
    if request.method != 'POST':
        return f'{request.method} not allowed', 405

    # Read the POST data
    app.logger.info('POST request to /purposes')
    data = request.get_json()
    app.logger.info(f'POST Data: {json.dumps(data)}')

    # Create the Purpose
    resp = telco_.create_purpose(data)

    # Store the newly created Purpose
    app.logger.info(f'Created Purpose {resp}')

    return jsonify(resp), 200

@app.route('/purposes/<id_>', methods=['GET'])
def get_purposes_by_id(id_):
    if request.method != 'GET':
        return f'{request.method} not allowed', 405

    app.logger.info(f'GET request to /purposes for id = {id_}')

    # Get the Purpose
    app_ = telco_.get_purpose(id_)

    return f'Found Purpose {id_}:\n{json.dumps(app_)}\n', 200

@app.route('/purposes/<id_>', methods=['DELETE'])
def delete_purposes_by_id(id_):
    if request.method != 'DELETE':
        return f'{request.method} not allowed', 405

    app.logger.info(f'DELETE request to /purposes for id = {id_}')

    # Delete the Purpose
    telco_.delete_purpose(id_)
    app.logger.info(f'Deleted Purpose {id_}')

    return f'Deleted Purpose {id_}\n', 200

@app.route('/apps', methods=['POST'])
def create_app():
    if request.method != 'POST':
        return f'{request.method} not allowed', 405

    # Read the POST data
    app.logger.info('POST request to /apps')
    data = request.get_json()
    app.logger.info(f'POST Data: {json.dumps(data)}')

    # Create the App
    resp = telco_.create_app(data)

    # Store the newly created App
    app.logger.info(f'Created App {resp}')

    return resp, 200

@app.route('/apps/<id_>', methods=['GET'])
def get_apps_by_id(id_):
    if request.method != 'GET':
        return f'{request.method} not allowed', 405

    app.logger.info(f'GET request to /apps for id = {id_}')

    # Get the App
    app_ = telco_.get_app(id_)

    return f'Found App {id_}:\n{json.dumps(app_)}\n', 200

@app.route('/apps/<id_>', methods=['DELETE'])
def delete_apps_by_id(id_):
    if request.method != 'DELETE':
        return f'{request.method} not allowed', 405

    app.logger.info(f'DELETE request to /apps for id = {id_}')

    # Delete the App
    telco_.delete_app(id_)
    app.logger.info(f'Deleted App {id_}')

    return f'Deleted App {id_}\n', 200

@app.route('/connectivity', methods=['POST'])
def create_connectivity():
    if request.method != 'POST':
        return f'{request.method} not allowed', 405

    # Read the POST data
    app.logger.info('POST request to /connectivity')
    data = request.get_json()
    app.logger.info(f'POST Data: {json.dumps(data)}')

    # Create the QoD Session
    resp = telco_.create_qod_session(data)

    # Store the newly created QoD Session
    app.logger.info(f'Created QoD Session {resp["id"]}')

    return jsonify(resp), 200

@app.route('/connectivity/<id_>', methods=['GET'])
def get_connectivity_by_id(id_):
    if request.method != 'GET':
        return f'{request.method} not allowed', 405

    app.logger.info(f'GET request to /connectivity for id = {id_}')

    # Get the QoD Session
    qod_session = telco_.get_qod_session(id_)

    return f'Found QoD Session {id_}:\n{json.dumps(qod_session)}\n', 200

@app.route('/connectivity/<id_>', methods=['DELETE'])
def delete_connectivity_by_id(id_):
    if request.method != 'DELETE':
        return f'{request.method} not allowed', 405

    app.logger.info(f'DELETE request to /connectivity for id = {id_}')

    # Delete the QoD Session
    telco_.delete_qod_session(id_)

    # Delete the QoD Session
    app.logger.info(f'Deleted QoD Session {id_}')

    return f'Deleted QoD Session {id_}\n', 200        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
