from flask import Flask, request, jsonify
import hazelcast
import os
import sys


def stop_node(node):
    os.system(f"docker stop {node}")


app = Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) > 1 else 3001

node_ip = ""

if port == 3001:
    node_ip = ["192.168.0.103:5701"]
    node_id = "f36a91a6fdf71c4ab2d36e9835ab0849c20f7afabd27ac6723a9913893a52769"
elif port == 3002:
    node_ip = ["192.168.0.103:5702"]
    node_id = "336ea4f8280bfb75c366f2ec1830943a7e83b2ed807aaeb18d32831bc1ad15ec"
elif port == 3003:
    node_ip = ["192.168.0.103:5703"]
    node_id = "7b87be64d0c9d1a2000d016889d4c62fb174ea3af6dd1f96c62ccf164522e1e4"

client = hazelcast.HazelcastClient(cluster_name="lab2", cluster_members=node_ip)
messages_map = client.get_map("messages-map").blocking()


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
        stop_node(node_id)
