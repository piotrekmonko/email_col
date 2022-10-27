import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



message = Mail(
    from_email="Karol Michniewicz <krl.michniewicz@gmail.com>",
    to_emails="Karol Michniewicz <karol.michniewicz@autologyx.com>",
    subject="again",
    html_content="Special chars !@#$%^&*()")
try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
