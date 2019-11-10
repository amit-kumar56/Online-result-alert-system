API_KEY = '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'

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='amit1004199@gmail.com',
    to_emails='amit10041999@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))