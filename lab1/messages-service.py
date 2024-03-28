from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/message', methods=['GET'])
def default_response():
    return jsonify(message='Not implemented yet'), 200


if __name__ == '__main__':
    app.run(port=3002)
