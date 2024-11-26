import pika
import json
import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'


def send_email(message):
    with smtplib.SMTP('smtp.example.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = MIMEText(f"From user: {message['user_alias']}\nMessage: {
                       message['message']}")
        msg['Subject'] = 'New Message'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'recipient@example.com'
        smtp.send_message(msg)


def callback(ch, method, properties, body):
    message = json.loads(body)
    send_email(message)


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='screamed_messages')
channel.basic_consume(queue='screamed_messages',
                      on_message_callback=callback, auto_ack=True)
print('Publish Service: Waiting for messages...')
channel.start_consuming()
