from flask import Flask, request, jsonify
import hazelcast
import os
import sys
import consul

def stop_node(node):
    os.system(f"docker stop {node}")


app = Flask(__name__)

consul_client = consul.Consul(host='localhost', port=8500)
port = int(sys.argv[1]) if len(sys.argv) > 1 else 3001

consul_client.agent.service.register(
    service_id=str(port),
    address="/log",
    name="logging",
    port=port,
)

_, kv_info = consul_client.kv.get("hz_config")
cluster_info = eval(kv_info["Value"].decode("utf-8"))
node_ip = cluster_info["node"][str(port)]["node_ip"]
node_id = cluster_info["node"][str(port)]["node_id"]

client = hazelcast.HazelcastClient(cluster_name=cluster_info["cluster_name"], cluster_members=node_ip)
messages_map = client.get_map(cluster_info["map_name"]).blocking()


@app.route('/log', methods=['POST', 'GET'])
def log_message():
    if request.method == 'POST':
        data = request.json
        uuid = data.get('uuid')
        if uuid:
            print(f'id: {uuid}')
            print(f'msg: {data.get("msg")}')
            messages_map.put(uuid, data.get('msg'))
            return jsonify({'status': 'Message logged'}), 200
        else:
            return jsonify({'error': 'UUID not provided in the request'}), 400

    elif request.method == 'GET':
        return jsonify(list(messages_map.values())), 200


if __name__ == '__main__':
    try:
        app.run(port=port)
    except KeyboardInterrupt:
        consul_client.agent.service.deregister(str(port))
        stop_node(node_id)
