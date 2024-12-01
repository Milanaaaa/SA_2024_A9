from flask import Flask, request, jsonify
import requests

PUBLISH_SERVICE_URL = "http://publish_service:5003/process"

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    data['message'] = data['message'].upper()

    response = requests.post(PUBLISH_SERVICE_URL, json=data)

    if response.status_code >= 200 and response.status_code < 300:
        return jsonify({'status': 'Message forwarded',
                        'publish_response': response.json()})
    else:
        return jsonify({'status': 'error',
                        'error_details': response.text}), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
