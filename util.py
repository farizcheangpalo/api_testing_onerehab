import string
import random
from requests import Response
# from json import JSONDecodeError
from jsonschema import validate, SchemaError, ValidationError
import json
from serverapi import ServerApi
import data.login_uat as login
import data.url_extension as url_ext
import datetime

def print_pass_message(text=''):
    return print("\033[1;32;40m"+text)

def print_fail_message(text=''):
    return print("\033[1;31;40m"+text)

def r_lum():
    num = str(int(random.random()*10))
    if num == "":
        return 0
    else:
        return int(num)

def generate_nric(list_items=[]):
    str_digit = ""
    random_num = 0
    first_letter = random.choice('STGF')
    if first_letter == 'S' or first_letter == 'T':
        last_letter = ['J','Z','I','H','G','F','E','D','C','B','A']
    else:
        last_letter = ['X','W','U','T','R','Q','P','N','M','L','K']
    if first_letter == 'T' or first_letter == 'G':   
        random_num = 4
    else:
        random_num = 0
    for i in [2,7,6,5,4,3,2]:
        digit = r_lum()
        random_num = random_num + i * digit
        str_digit = str_digit + str(digit)
    last_letter = last_letter[random_num%11]
    nric = first_letter + str_digit + last_letter

def generate_dob(age=50):
    today = datetime.date.today()
    month = datetime.date.today().month
    day = datetime.date.today().day
    if str(month)=="2" and str(day)=="29":
        year = str(today).split("-")[0]
        birth_year = str(int(year) - age)
        dob = str(today).replace(year,birth_year)
        dob = str(today)[:8] + "28"
        return dob
    else:
        year = str(today).split("-")[0]
        birth_year = str(int(year) - age)
        dob = str(today).replace(year,birth_year)
        return dob


def sort_field_by(list={},field='',is_asc=True,page_size=20):
    arr = []
    for item in list:
        arr.append(item[field])
    
    if not field == 'fullName':
        if is_asc:
            arr.sort(reverse=False)
        else:
            arr.sort(reverse=True)
        return arr[:page_size]
    else:
        if not is_asc:
            arr.reverse()
        return arr[:page_size]

def store_response_sort_by(list={},field=''):
    arr = []
    for item in list:
        arr.append(item[field])
    return arr

def assert_sort_by(list={}, type='active', sort_by='', is_asc=True, field=''):
    API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
    client = ServerApi(api_url=API_URL)
    request_json = read_json_file("data/json/request/{}_list.json".format(type))

    details = get_details_after_login(login.EMAIL,login.DOMAIN)
    request_json['organization'] = details['orgCenterResponseCode']
    request_json['sortBy'] = [sort_by]
    response = client.post_with_bearer_token(request_json)
    
    assert response.status_code == 200

    fullname_arr = store_response_sort_by(response.json()["items"],field=field)
    expected_arr = sort_field_by(list=list,field=field,is_asc=is_asc,page_size=request_json['pageSize'])
    
    assert fullname_arr == expected_arr

def get_details_after_login(email=None, domain=None, subdomain=None):
    if email=="admincsp" and domain=="healthgrp" and subdomain==None:
        return {
                    "userId": "e8c95a8e49aa4e968e7327ff85b1c419",
                    "subOrgResponseName": "OneRehab CSP",
                    "subOrgResponseCode": "OneRehab_CSP",
                    "orgCenterResponseName": "OneRehab-CSP-Center",
                    "orgCenterResponseCode": "OneRehab_CSP_Center"
                }

def read_json_file(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def get_all_active_list(total_page=None):
    login.ACTIVE_LIST_ITEMS = []
    details = get_details_after_login(login.EMAIL,login.DOMAIN)
    for i in range(total_page):
        API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
        client = ServerApi(api_url=API_URL)
        request_json = read_json_file("data/json/request/active_list.json")
        request_json['organization'] = details['orgCenterResponseCode']
        request_json['page'] = i+1

        response = client.post_with_bearer_token(request_json)

        for item in response.json()['items']:
            login.ACTIVE_LIST_ITEMS.append(item)

    return login.ACTIVE_LIST_ITEMS

def get_all_discharged_list(total_page=None):
    login.DISCHARGED_LIST_ITEMS = []
    details = get_details_after_login(login.EMAIL,login.DOMAIN)
    for i in range(total_page):
        API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
        client = ServerApi(api_url=API_URL)
        request_json = read_json_file("data/json/request/discharged_list.json")
        request_json['organization'] = details['orgCenterResponseCode']
        request_json['page'] = i+1

        response = client.post_with_bearer_token(request_json)

        for item in response.json()['items']:
            login.DISCHARGED_LIST_ITEMS.append(item)

    return login.DISCHARGED_LIST_ITEMS

# def update_discharged_list(total_records=None, current_page_number=None, \
#                         total_page=None, items=[]):
#     local.DISCHARGED_LIST_TOTAL_RECORDS = total_records
#     local.DISCHARGED_LIST_TOTAL_PAGE = total_page
#     local.DISCHARGED_LIST_ITEMS = items

#     return local.DISCHARGED_LIST_ITEMS



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

