import os
import json
import base64
import re

from sendgrid import SendGridAPIClient


_sendgrid_client = None


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


def get_sendgrid_client():
    global _sendgrid_client
    if not _sendgrid_client:
        _sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    return _sendgrid_client


def send_message(case_message):
    sendgrid_client = get_sendgrid_client()
    response = sendgrid_client.send(case_message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


def process_cases(cases):
    for case in cases:
        case_message = process_case(case)
        send_message(case_message)


def process_json(json_file_path):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        html_content = data['html_content']
        plain_content = re.sub('<[^<]+?>', '', html_content)
        return {
            'from': {
                'email': data['from_email'],
            },
            'personalizations': [{
                'to': [{
                    'email': data['to_email']
                }],
                'subject': data['subject'],
            }],
            'content': [
                {
                    'type': 'text/plain',
                    'value': plain_content,
                },
                {
                    'type': 'text/html',
                    'value': html_content,
                },
            ]
        }


def process_attachment(attachment_path):
    with open(attachment_path, 'rb') as src:
        file_name, extension = os.path.basename(attachment_path).rsplit('.', 1)
        return {
            'content': base64.b64encode(src.read()).decode('utf-8'),
            'content_id': str(hash(attachment_path)),
            'disposition': 'attachment',
            'filename': os.path.basename(attachment_path),
            'name': file_name,
            'type': extension,
        }


def process_case(case):
    print('processing %s' % case)
    files = os.listdir(case)
    message = {}
    attachments = []
    # build message and attachments
    for file_path in files:
        file_path = os.path.join(case, file_path)
        if file_path.endswith(".json"):
            message.update(process_json(file_path))
        else:
            att = process_attachment(file_path)
            if att:
                attachments.append(att)
    print('message:', message)
    print('attachments:', len(attachments))
    if len(attachments):
        message['attachments'] = attachments
    return message


if __name__ == '__main__':
    cases = get_cases()
    cases.sort()
    process_cases(cases)
