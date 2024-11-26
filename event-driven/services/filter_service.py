import pika
import json

STOP_WORDS = {'bird-watching', 'ailurophobia', 'mango'}


def callback(ch, method, properties, body):
    message = json.loads(body)
    if any(word in message['message'] for word in STOP_WORDS):
        print("Message filtered out:", message['message'])
        return
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='filtered_messages')
    channel.basic_publish(
        exchange='', routing_key='filtered_messages', body=json.dumps(message))
    connection.close()


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='incoming_messages')
channel.basic_consume(queue='incoming_messages',
                      on_message_callback=callback, auto_ack=True)
print('Filter Service: Waiting for messages...')
channel.start_consuming()
