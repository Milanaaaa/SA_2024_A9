from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)


def send_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='incoming_messages')
    channel.basic_publish(
        exchange='', routing_key='incoming_messages', body=json.dumps(message))
    connection.close()


@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'message' not in data or 'user_alias' not in data:
        return jsonify({'error': 'Invalid payload'}), 400
    send_to_queue(data)
    return jsonify({'status': 'Message sent'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
