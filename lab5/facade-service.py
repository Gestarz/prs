import uuid
import requests
import random
import hazelcast
from flask import Flask, jsonify, request
import consul
import sys

app = Flask(__name__)

# MESSAGES_SERVICE_URLS = [
#     "http://localhost:3004/message",
#     "http://localhost:3005/message"]
# LOGGING_SERVICE_URLS = [
#     "http://localhost:3001/log",
#     "http://localhost:3002/log",
#     "http://localhost:3003/log"
# ]


port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

client = hazelcast.HazelcastClient(cluster_name="lab2")
consul_client = consul.Consul(host='localhost', port=8500)
consul_client.agent.service.register(
    service_id=str(port),
    address="/facade",
    name="facade",
    port=port,
)

_, LOGGING_SERVICE_CONSUL = consul_client.health.service("logging")
LOGGING_SERVICE_URLS = [f'http://127.0.0.1:{el["Service"]["Port"]}{el["Service"]["Address"]}' for el in LOGGING_SERVICE_CONSUL]
_, MESSAGES_SERVICE_CONSUL = consul_client.health.service("message")
MESSAGES_SERVICE_URLS = [f'http://127.0.0.1:{el["Service"]["Port"]}{el["Service"]["Address"]}' for el in MESSAGES_SERVICE_CONSUL]



_, kv_info = consul_client.kv.get("hz_config")
cluster_info = eval(kv_info["Value"].decode("utf-8"))

queue = client.get_queue(cluster_info["queue_name"]).blocking()


@app.route('/facade', methods=['POST', 'GET'])
def message():
    if request.method == 'POST':
        logging_service_url = random.choice(LOGGING_SERVICE_URLS)
        message_service_url = random.choice(MESSAGES_SERVICE_URLS)
        message = request.data.decode('utf-8')
        queue.put(message)
        requests.post(message_service_url)
        unique_id = str(uuid.uuid4())
        response = requests.post(logging_service_url, json={'uuid': unique_id, 'msg': message})
        return jsonify({'uuid': unique_id, 'response': response.json()}), response.status_code
    elif request.method == 'GET':
        print("LOGGING_SERVICE_URLS: ", LOGGING_SERVICE_URLS)
        print("MESSAGES_SERVICE_URLS: ", MESSAGES_SERVICE_URLS)
        logging_service_url = random.choice(LOGGING_SERVICE_URLS)
        message_service_url = random.choice(MESSAGES_SERVICE_URLS)
        messages_response = requests.get(message_service_url)
        log_response = requests.get(logging_service_url)
        logged_messages = " ".join(log_response.json()) if log_response.status_code == 200 else []
        queue_messages = messages_response.json() if messages_response.status_code == 200 else []
        return jsonify({'logged_messages': logged_messages, 'message_response': queue_messages}), 200


if __name__ == '__main__':
    try:
        app.run(port=port)
    except KeyboardInterrupt:
        consul_client.agent.service.deregister(str(port))
