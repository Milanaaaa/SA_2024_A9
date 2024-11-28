from flask import Flask, request, jsonify
import requests
import json

# Define downstream service endpoint (publish_service)
PUBLISH_SERVICE_URL = "http://publish_service:5003/process"

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()

    # Check for invalid payloads
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    # Transform the message
    data['message'] = data['message'].upper()
    print(f"SCREAMING Service: Transformed Message: {data}")

    # Forward to publish_service
    response = requests.post(PUBLISH_SERVICE_URL, json=data)
    return jsonify({'status': 'Message forwarded', 'publish_response': response.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)