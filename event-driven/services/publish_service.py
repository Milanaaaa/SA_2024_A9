import pika
import json
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

recipients = [
    "mikhail_kalinin_a@mail.ru",
    "fragile_cat@mail.ru",
    "emi.gaynulllin@gmail.com",
]


def send_email(message):
    with SMTP_SSL("smtp.mail.ru", 465) as smtp:
        smtp.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

        msg = MIMEText(
            f"From user: {message['user_alias']}\n"
            f"Message: {message['message']}"
        )

        msg["Subject"] = "SoftArch assignment"

        for rec in recipients:
            smtp.sendmail(EMAIL_ADDRESS, rec, msg.as_string())


def callback(ch, method, properties, body):
    message = json.loads(body)
    send_email(message)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", port=5672)
    )

    channel = connection.channel()

    channel.queue_declare(queue="screamed_messages")

    channel.basic_consume(
        queue="screamed_messages", on_message_callback=callback, auto_ack=True
    )

    print("Publish Service: Waiting for messages...")

    channel.start_consuming()


if __name__ == '__main__':
    main()
