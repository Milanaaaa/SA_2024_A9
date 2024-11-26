import pika
import json


def callback(ch, method, properties, body):
    message = json.loads(body)
    message['message'] = message['message'].upper()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='screamed_messages')
    channel.basic_publish(
        exchange='', routing_key='screamed_messages', body=json.dumps(message))
    connection.close()


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()
channel.queue_declare(queue='filtered_messages')
channel.basic_consume(queue='filtered_messages',
                      on_message_callback=callback, auto_ack=True)
print('SCREAMING Service: Waiting for messages...')
channel.start_consuming()
