from flask import Flask, jsonify, request
import sys
import hazelcast

port = int(sys.argv[1]) if len(sys.argv) > 1 else 3004

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_name="lab2")
queue = client.get_queue("msq_queue").blocking()

messages = []

@app.route('/message', methods=['GET', 'POST'])
def default_response():
    if request.method == 'POST':
        msg = queue.take()
        print(f"Get message {msg}")
        messages.append(msg)
        return jsonify('Get message'), 200
    elif request.method == 'GET':
        return jsonify(f"Messages on port {port}: {messages}"), 200


if __name__ == '__main__':
    app.run(port=port)
