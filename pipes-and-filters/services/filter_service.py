from flask import Flask, request, jsonify
import requests
import json

# Define downstream service endpoint (screaming_service)
SCREAMING_SERVICE_URL = "http://screaming_service:5002/process"

STOP_WORDS = ["bird-watching", "ailurophobia", "mango"]

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()

    # Check for invalid payloads
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    # Apply filtering logic
    if any(word in data["message"] for word in STOP_WORDS):
        print(f"Filter Service: Message filtered out: {data['message']}")
        return jsonify({'status': 'Filtered out'}), 200

    # Forward to screaming_service
    response = requests.post(SCREAMING_SERVICE_URL, json=data)
    print("Filter Service: Forwarded message to screaming service")
    return jsonify({'status': 'Message forwarded', 'screaming_response': response.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)