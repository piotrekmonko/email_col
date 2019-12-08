import os
import json
import base64
import collections
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pprint



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
        subj = os.path.basename(item)
        from_address = []
        to = []
        content = []
        files = os.listdir(item)
        for file in files:
            file_path = os.path.join(item, file)
            if file.endswith(".json"):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    from_address.append(data['from_email'])
                    to.append(data['to_email'])
                    content.append(data['html_content'])

        message = Mail(
            from_email=str(from_address[0]),
            to_emails=str(to[0]),
            subject=(subj[0]),
            html_content=(content[0])
        )

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


email(get_cases())
