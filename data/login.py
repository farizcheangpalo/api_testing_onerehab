# UAT base url
API_URL = 'https://onerehab-uat.iconnect.care'
# API_URL = 'http://localhost:3000/onerehab/'

# email/username
EMAIL = "admincsp"

# email verifier (might need to update from time to time)
EMAILVERIFIER = "obO9lb2TImMPf5UNye+KKVk8XNp7aMHuMXi3FNGabfnAwMSAw4WuZ790Uh/Cv65Qgde/Gl3abjT8+/xEC0XAe3Rmy5AYRGep3ibdj5B9kSGHRUoJrjmpq+b8Wh67u6vragjU6DhLwyHzIgggZvbNn12+WCtJfPwD71rFBonxQNXsbi2aDS4o2Lyy5Qjwzd+WhjFnSCV11NqG5iCmIQgRBDb2eb1LmJp5Z6BQB2FX9QoRQqQb5yIb1Bw3JFfNE+i9+GNXZzqSmuC5CkEn7DMldGiyh8uDvx3+MJNyqNvdJjrBdn4MXIAccTvQ6qufXKi6vK5vgUjjH3WrlA/5bJCINA=="

# domain
DOMAIN = "healthgrp"

# # subdomain
# SUBDOMAIN = "SINGHEALTH"

# global access token
# this will be stored after the login and shared throughout the files
global ACCESS_TOKEN
ACCESS_TOKEN = ""

# ACTIVE LIST 
global ACTIVE_LIST_TOTAL_RECORDS
ACTIVE_LIST_TOTAL_RECORDS = None

global ACTIVE_LIST_CURRENT_PAGE_NUMBER
ACTIVE_LIST_CURRENT_PAGE_NUMBER = None

global ACTIVE_LIST_TOTAL_PAGE
ACTIVE_LIST_CURRENT_PAGE_NUMBER = None

global ACTIVE_LIST_ITEMS
ACTIVE_LIST_ITEMS = []

# DISCHARGED LIST 
global DISCHARGED_LIST_TOTAL_RECORDS
DISCHARGED_LIST_TOTAL_RECORDS = None

global DISCHARGED_LIST_CURRENT_PAGE_NUMBER
DISCHARGED_LIST_CURRENT_PAGE_NUMBER = None

global DISCHARGED_LIST_TOTAL_PAGE
DISCHARGED_LIST_CURRENT_PAGE_NUMBER = None

global DISCHARGED_LIST_ITEMS
DISCHARGED_LIST_ITEMS = []

SORT_BY = {
    "fullname_asc": {"field": "FullName", "direction": "Asc"},
    "fullname_desc": {"field": "FullName", "direction": "Desc"},
    "dateofbirth_asc": {"field": "DateofBirth", "direction": "Asc"},
    "dateofbirth_desc": {"field": "DateofBirth", "direction": "Desc"},
    "nric_asc": {"field": "Nric", "direction": "Asc"},
    "nric_desc": {"field": "Nric", "direction": "Desc"}
}

global TRACE_ID
TRACE_ID = ""

# ASSIGNEE = "abc@noDomain.com"
# REPORTER = "xyz@nodomain.com"
# DESCRIPTION = "Please go through the API documentation and write the integration test for the APIs. Try to cover all possible scenarios.",
# DUEDATE = "2020-11-30"

# POST_TASK_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "taskId": {"type": "number"},
#         "assignee": {"type": "string"},
#         "reporter": {"type": "string"},
#         "description": {"type": "string"},
#         "dueDate": {"type": "string"}
#     }
# }

# GET_TASK_SCHEMA = {
#     "type": "array",
#     "items": [
#         {
#             "type": "object",
#             "properties": {
#                 "taskId": {"type": "number"},
#                 "assignee": {"type": "string"},
#                 "reporter": {"type": "string"},
#                 "description": {"type": "string"},
#                 "dueDate": {"type": "string"}
#             }
#         }
#     ]
# }

# GET_TASK_ID_SCHEMA = POST_TASK_SCHEMA