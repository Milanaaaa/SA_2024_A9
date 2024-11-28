import pika
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

FILTER_SERVICE_URL = "http://filter_service:5001/process"


def send_to_queue(message):
    requests.post(FILTER_SERVICE_URL, json=message)


@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()

    if (
            not data
            or 'message' not in data
            or 'user_alias' not in data
    ):
        return jsonify({'error': 'Invalid payload'}), 400

    send_to_queue(data)

    return jsonify({'status': 'Message sent'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
