from flask import Flask, request, jsonify
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from enum import Enum

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


class EmailStatus(Enum):
    SUCCESS = "Success"
    ERROR = "General Error"


recipients = [
    "mikhail_kalinin_a@mail.ru",
    "fragile_cat@mail.ru",
    "emi.gaynulllin@gmail.com",
]

app = Flask(__name__)


def send_email(message):
    try:
        with SMTP_SSL("smtp.mail.ru", 465) as smtp:
            smtp.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

            msg = MIMEText(
                f"From user: {message['user_alias']}\n"
                f"Message: {message['message']}"
            )

            msg["Subject"] = "SoftArch assignment"

            for recipient in recipients:
                smtp.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        return EmailStatus.SUCCESS
    except Exception:
        return EmailStatus.ERROR


@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()

    if not data or 'message' not in data or 'user_alias' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    match send_email(data):
        case EmailStatus.SUCCESS:
            return jsonify({'status': 'Email sent'})
        case EmailStatus.ERROR:
            return jsonify({'status': 'Email could not be sent'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
