from flask import Flask, request, jsonify
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

recipients = [
    "mikhail_kalinin_a@mail.ru",
    "fragile_cat@mail.ru",
    "emi.gaynulllin@gmail.com",
]

app = Flask(__name__)

def send_email(message):
    with SMTP_SSL("smtp.mail.ru", 465) as smtp:
        smtp.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

        msg = MIMEText(
            f"From user: {message['user_alias']}\n"
            f"Message: {message['message']}"
        )

        msg["Subject"] = "SoftArch assignment"

        for recipient in recipients:
            smtp.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        print(f"Email sent to {', '.join(recipients)} for message: {message}")

@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()

    # Check for invalid payloads
    if not data or 'message' not in data or 'user_alias' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    # Send the email
    send_email(data)
    return jsonify({'status': 'Email sent'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)