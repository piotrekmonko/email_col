import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="krl.michniewicz@gmail.com",
    to_emails="karol.michniewicz@autologyx.com",
    subject="Normal email without attachment",
    html_content="<strong>Email content</strong>")
try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
