import string
import random
from requests import Response
# from json import JSONDecodeError
from jsonschema import validate, SchemaError, ValidationError
import json

def get_details_after_login(email=None, domain=None, subdomain=None):
    if email=="admincsp" and domain=="healthgrp" and subdomain==None:
        return {
                    "userId": "e8c95a8e49aa4e968e7327ff85b1c419",
                    "subOrgResponseName": "OneRehab CSP",
                    "subOrgResponseCode": "OneRehab_CSP",
                    "orgCenterResponseName": "OneRehab-CSP-Center",
                    "orgCenterResponseCode": "OneRehab-CSP-Center"
                }

def read_json_file(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


# def text_to_json(text):
#     return json.dumps(text)


# def compose_response_msg(response: Response):
#     req = response.request
#     req_body = ''
#     if isinstance(req.body, str):
#         req_body = req.body
#     elif isinstance(req.body, bytearray) or isinstance(req.body, bytes):
#         req_body = req.body.decode(encoding='utf8')

#     request_id = req.headers.get('X-Request-Id', '')

#     return 'Request(id: {request_id}) \n  {method} {url} {req_body} RETURNS \n  Response [{status}] {resp_body}' \
#         .format(request_id=request_id,
#                 method=req.method,
#                 url=response.url,
#                 req_body=req_body,
#                 status=response.status_code,
#                 resp_body=response.text)


# def json_schema_check(response, schema, expected_status=200, resolver=None):
#     assert response.status_code == expected_status, \
#         'Failed to check status code, expected: {}. {}'.format(expected_status, compose_response_msg(response))
#     try:
#         json_response = response.json()
#     except ValueError or JSONDecodeError:
#         json_response = None
#     if schema is None:
#         assert json_response is None or json_response == "", \
#             'A None schema should match with a None response. {}'.format(compose_response_msg(response))
#     elif len(schema) == 0:
#         assert json_response is not None and len(json_response) == 0, \
#             'An empty schema should match with an empty response. {}'.format(compose_response_msg(response))
#     else:
#         try:
#             validate(json_response, schema, resolver=resolver)
#         except Exception as error:
#             assert not isinstance(error, SchemaError), \
#                 'Schema is invalid. Please check it.\n{}'.format(error)
#             assert not isinstance(error, ValidationError), \
#                 'Schema check failed. {}\n{}'.format(compose_response_msg(response), error)
#             raise error


# def generate_random_string(length):
#     letters = string.ascii_lowercase
#     result_str = ''.join(random.choice(letters) for _ in range(length))
#     return result_str


# def generate_random_date():
#     day = random.randint(1, 30)
#     if day < 10:
#         day = '0{}'.format(day)
#     else:
#         day = str(day)
#     month = random.randint(1, 12)
#     if month < 10:
#         month = '0{}'.format(month)
#     else:
#         month = str(month)
#     year = str(random.randint(2020, 2030))
#     return '{}-{}-{}'.format(year, month, day)

