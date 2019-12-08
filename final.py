import os
import json
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


def get_cases():
    cwd = os.getcwd()  # get current path
    cases_folder = "mail_cases"  # test cases main folder
    cases = []
    main_path = os.path.join(cwd, cases_folder)

    for root, dirs, files in os.walk(main_path):
        for name in dirs:
            cases.append(os.path.join(root, name))
            # print(os.path.join(root, name))

    return cases


def email(cases):
    for item in cases:
        subj = []
        from_address = []
        to = []
        content = []
        encoded_base = []
        files = os.listdir(item)
        for file in files:
            file_path = os.path.join(item, file)
            if file.endswith(".json"):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    from_address.append(data['from_email'])
                    to.append(data['to_email'])
                    content.append(data['html_content'])
                    subj.append(data['subject'])
            elif file.endswith(".pdf"):
                with open(file_path, 'rb') as f:
                    data = f.read()
                    f.close()
                encoded_base.append(base64.b64encode(data).decode())

        message = Mail(
            from_email=str(from_address[0]),
            to_emails=str(to[0]),
            subject=str(subj[0]),
            html_content=(content[0])
        )

        if len(encoded_base) == 0:
            pass
        else:
            attachment = Attachment()
            attachment.file_content = FileContent(encoded_base[0])  # The Base64 encoded content of the attachment
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


email(get_cases())
