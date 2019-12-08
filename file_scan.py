import os
import json
import base64
import collections


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

    # email_data = collections.defaultdict(dict)

    for item in cases:
        case_name = os.path.basename(item)

        fin = {case_name: ""}

        case_data = collections.defaultdict(dict)

        print(case_name)
        email_body = collections.defaultdict(dict)
        email_attach = collections.defaultdict(dict)
        files = os.listdir(item)
        for file in files:
            file_path = os.path.join(item, file)
            if file.endswith(".json"):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    email_body[file] = data
            else:
                email_attach[file] = file_path
        case_data[case_name] =

            #elif file.endswith(".pdf"):
             #   with open(file_path) as pdf_file:
              #      pdf_encoded = base64.b64encode(pdf_file).decode()
               #     email_attach[file] = pdf_encoded




        print(email_body)
        print(email_attach)



email_payload(get_cases())

