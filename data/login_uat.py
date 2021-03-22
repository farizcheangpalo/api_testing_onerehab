# UAT base url
API_URL = 'https://onerehab-uat.iconnect.care'

# email/username
EMAIL = "admincsp"

# email verifier (might need to update from time to time)
EMAILVERIFIER = "gxdruSmnF/qOhXE3juYxArA0vgVGZynWwWVLx9cPIJ69z82ybtOK6vNt+LQqDt7DDdXNxwi4DgVM/OQwf6Tdd4WMv2lQN2WZMzdNuB+KVhW3Oh2h53cORQgq6Ki7GXH+hd96E8Ry9APERA0T28HrbyIJNcQNMEyVAFwjEPmoqOhvSyOnqFuPI9i+OvtmCghZp4AiWSEXud4NRaURWvbpZnuFS3KSkdRv38bR37fzRHwk+EMVFtDcKXzrgNLAIx92igg17YloczUPykMKlJjXoJubFTlVgeEPv0oZprrvc4eo4CQNypqOWV8fWZfDDmcD2VBtIsneFBA1LMyUIxwKKw=="

# domain
DOMAIN = "healthgrp"

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