from flask import Flask, request, jsonify
import hazelcast
import os


def stop_node(node):
    os.system(f"docker stop {node}")


app = Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) > 1 else 3001

node_ip = ""

if port == 3001:
    node_ip = ["192.168.0.102:5701"]
    node_id = "cd73be79d30b68b31907764fde0d2cd8168852e788fabc58c197113b268aa756"
elif port == 3002:
    node_ip = ["192.168.0.102:5702"]
    node_id = "d9ee4384d4eae646d450113b4346e44037769653aa0ea266b5e6e255b22411d3"
elif port == 3003:
    node_ip = ["192.168.0.102:5703"]
    node_id = "74ff39a5a895634e848324df1838f0df14d1acfadc73b336b8d66e3709363d50"

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
