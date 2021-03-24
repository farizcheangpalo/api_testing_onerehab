from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login as login
import data.url_extension as url_ext
import util
from parameterized import parameterized, parameterized_class
import random

# verify that search existing patients is correct
def test_post_search_existing():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SEARCH)
    client = ServerApi(api_url=API_URL)

    is_all_pass = True
    count=0

    list_items = []

    for item in login.ACTIVE_LIST_ITEMS:
        list_items.append(item)
    for item in login.DISCHARGED_LIST_ITEMS:
        list_items.append(item)

    for item in list_items:
        response = client.post_with_bearer_token(
                        {
                            "nric": item['nric'],
                            "dateOfBirth": item['dateofBirth'].split("T")[0]
                        }
                    )
        try:
            assert response.status_code == 200
            assert response.json()['id'] == item['id']
            assert response.json()['nric'] == item['nric']
            assert response.json()['dateofBirth'] == item['dateofBirth']
            assert response.json()['fullName'] == item['fullName']
            assert response.json()['gender'] == item['gender']

            if count==0:
                util.print_pass_message("\ntest_post_search_existing {} {} PASSED ".format(item['id'],item['fullName']))
            else:
                util.print_pass_message("test_post_search_existing {} {} PASSED ".format(item['id'],item['fullName']))
        except:
            is_all_pass &= False
            
            if count==0:
                util.print_fail_message("\ntest_post_search_existing {} {} FAILED".format(item['id'],item['fullName']))
            else:
                util.print_fail_message("test_post_search_existing {} {} FAILED".format(item['id'],item['fullName']))

        count+=1
    
    assert is_all_pass == True

# verify that search new patients is correct
def test_post_search_new():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SEARCH)
    client = ServerApi(api_url=API_URL)

    count=0
    
    nric = util.generate_nric()
    response = client.post_with_bearer_token(
                    {
                        "nric": nric,
                        "dateOfBirth": util.generate_dob(random.randint(1,100))
                    }
                )

    assert response.status_code == 200
    assert response.json()['title'] == "Patient with NRIC '{}' was not found".format(nric)

    login.TRACE_ID = response.json()['traceId']