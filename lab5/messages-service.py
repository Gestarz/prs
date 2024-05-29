from flask import Flask, jsonify, request
import sys
import hazelcast
import consul

port = int(sys.argv[1]) if len(sys.argv) > 1 else 3004

app = Flask(__name__)

consul_client = consul.Consul(host='localhost', port=8500)
consul_client.agent.service.register(
    service_id=str(port),
    address="/message",
    name="message",
    port=port
)

_, kv_info = consul_client.kv.get("hz_config")
cluster_info = eval(kv_info["Value"].decode("utf-8"))

client = hazelcast.HazelcastClient(cluster_name=cluster_info["cluster_name"])
queue = client.get_queue(cluster_info["queue_name"]).blocking()

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
    try:
        app.run(port=port)
    except KeyboardInterrupt:
        consul_client.agent.service.deregister(str(port))
