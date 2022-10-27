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


def email_payload(cases):

    email_data = []

    for item in cases:
        case_name = os.path.basename(item)
        case_data = collections.defaultdict(dict)
        email_body = collections.defaultdict(dict)
        email_attach = {}
        files = os.listdir(item)
        for file in files:
            file_path = os.path.join(item, file)
            if file.endswith(".json"):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    email_body[file] = data
            else:
                email_attach[file] = file_path
        email_body.update(email_attach)
        case_data[case_name] = email_body
        email_data.append(case_data)

    return email_data


def send_mail(email_data):

    klucze = []
    final = []

    for item in email_data:
        app_json2 = json.dumps(item)
        newobj = json.loads(app_json2)
        klucze.append(newobj)
        #print(newobj)
        for key in newobj:
            jsonkey = key + '.json'
        #    print(jsonkey)

    for item in klucze:
        print(item)


'''
    for item in klucze:
       for key in item:
           final.append(key)

    for item in final:
        



    message = Mail(

    )
'''


#email_payload(get_cases())
send_mail(email_payload(get_cases()))

