from flask import Flask, request, jsonify
import requests

SCREAMING_SERVICE_URL = "http://screaming_service:5002/process"

STOP_WORDS = ["bird-watching", "ailurophobia", "mango"]

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    if any(word in data["message"] for word in STOP_WORDS):
        return jsonify({'status': 'Filtered out'}), 200

    response = requests.post(SCREAMING_SERVICE_URL, json=data)

    if response.status_code >= 200 and response.status_code < 300:
        return jsonify({'status': 'Message forwarded',
                        'screaming_response': response.json()})
    else:
        return jsonify({'status': 'error',
                        'error_details': response.text}), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
