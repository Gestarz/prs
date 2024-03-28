from flask import Flask, request, jsonify

app = Flask(__name__)
messages = {}


@app.route('/log', methods=['POST', 'GET'])
def log_message():
    if request.method == 'POST':
        data = request.json
        uuid = data.get('uuid')
        if uuid:
            messages[uuid] = data.get('msg')
            return jsonify({'status': 'Message logged'}), 200
        else:
            return jsonify({'error': 'UUID not provided in the request'}), 400

    elif request.method == 'GET':
        return jsonify(list(messages.values())), 200


if __name__ == '__main__':
    app.run(port=3001)
