import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

FILTER_SERVICE_URL = "http://filter_service:5001/process"


@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()

    if (
            not data
            or 'message' not in data
            or 'user_alias' not in data
    ):
        return jsonify({'error': 'Invalid payload'}), 400

    response = requests.post(FILTER_SERVICE_URL, json=data)

    if response.status_code >= 200 and response.status_code < 300:
        return jsonify({'status': 'Message forwarded',
                        'filter_response': response.json()})
    else:
        return jsonify({'status': 'error',
                        'error_details': response.text}), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
