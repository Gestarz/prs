import uuid
import requests
import random

from flask import Flask, jsonify, request

app = Flask(__name__)

MESSAGES_SERVICE_URL = "http://localhost:3005/message"
LOGGING_SERVICE_URLS = [
    "http://localhost:3001/log",
    "http://localhost:3002/log",
    "http://localhost:3003/log"
]

@app.route('/facade', methods=['POST', 'GET'])
def message():
    if request.method == 'POST':
        logging_service_url = random.choice(LOGGING_SERVICE_URLS)
        message = request.data.decode('utf-8')
        unique_id = str(uuid.uuid4())
        response = requests.post(logging_service_url, json={'uuid': unique_id, 'msg': message})
        return jsonify({'uuid': unique_id, 'response': response.json()}), response.status_code
    elif request.method == 'GET':
        logging_service_url = random.choice(LOGGING_SERVICE_URLS)
        messages_response = requests.get(MESSAGES_SERVICE_URL)
        log_response = requests.get(logging_service_url)
        logged_messages = " ".join(log_response.json()) if log_response.status_code == 200 else []
        static_message = messages_response.json() if messages_response.status_code == 200 else []
        return jsonify({'logged_messages': logged_messages, 'default_response': static_message}), 200

if __name__ == '__main__':
    app.run(port=3000)
