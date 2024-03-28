import uuid
import requests

from flask import Flask, jsonify, request

app = Flask(__name__)

LOGGING_SERVICE_URL = "http://localhost:3001/log"
MESSAGES_SERVICE_URL = "http://localhost:3002/message"


@app.route('/facade', methods=['POST', 'GET'])
def message():
    if request.method == 'POST':
        message = request.data.decode('utf-8')
        unique_id = str(uuid.uuid4())
        response = requests.post(LOGGING_SERVICE_URL, json={'uuid': unique_id, 'msg': message})
        return jsonify({'uuid': unique_id, 'response': response.json()}), response.status_code
    elif request.method == 'GET':
        log_response = requests.get(LOGGING_SERVICE_URL)
        messages_response = requests.get(MESSAGES_SERVICE_URL)
        logged_messages = " ".join(log_response.json()) if log_response.status_code == 200 else []
        static_message = messages_response.json() if messages_response.status_code == 200 else []
        return jsonify({'logged_messages': logged_messages, 'default_response  ': static_message}), 200

if __name__ == '__main__':
    app.run(port=3000)
