import base64
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
import urllib.request as urllib


import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="krl.michniewicz@gmail.com",
    to_emails="karol.michniewicz@autologyx.com",
    subject="Normal email without attachment",
    html_content="<strong>Email content</strong>"
)

file_path = 'C:\\Users\\dean\\Desktop\\email_collector\\mail_files\\example.pdf'


with open(file_path, 'rb') as f:
    data = f.read()
    f.close()

encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)  # The Base64 encoded content of the attachment
attachment.file_type = FileType('application/pdf')  # The MIME type of the content you are attaching
attachment.file_name = FileName('test_filename.pdf')  # The filename of the attachment
attachment.disposition = Disposition('attachment')  # Attachment or Inline (inside emails body)
attachment.content_id = ContentId('Example Content ID')  # Only used for Disposition(inline)
message.attachment = attachment


try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
