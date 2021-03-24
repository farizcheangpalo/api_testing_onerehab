from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login as login
import data.url_extension as url_ext
import util
from parameterized import parameterized, parameterized_class

# verify that active patients profile details are correct
def test_post_active_patient_profile():
    API_URL = "{}/{}".format(login.API_URL,url_ext.PROFILE)
    client = ServerApi(api_url=API_URL)

    is_all_pass = True
    count=0

    for item in login.ACTIVE_LIST_ITEMS:
        response = client.post_with_bearer_token(
                        {
                            "patientId": item['id'],
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
                util.print_pass_message("\ntest_post_active_patient_profile {} {} PASSED ".format(item['id'],item['fullName']))
            else:
                util.print_pass_message("test_post_active_patient_profile {} {} PASSED ".format(item['id'],item['fullName']))
        except:
            is_all_pass &= False
            
            if count==0:
                util.print_fail_message("\ntest_post_active_patient_profile {} {} FAILED".format(item['id'],item['fullName']))
            else:
                util.print_fail_message("test_post_active_patient_profile {} {} FAILED".format(item['id'],item['fullName']))

        count+=1

    assert is_all_pass == True

# verify that discharged patients profile details are correct
def test_post_discharged_patient_profile():
    API_URL = "{}/{}".format(login.API_URL,url_ext.PROFILE)
    client = ServerApi(api_url=API_URL)

    is_all_pass = True
    count=0

    for item in login.DISCHARGED_LIST_ITEMS:
        response = client.post_with_bearer_token(
                        {
                            "patientId": item['id'],
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
                util.print_pass_message("\ntest_post_discharged_patient_profile {} {} PASSED ".format(item['id'],item['fullName']))
            else:
                util.print_pass_message("test_post_discharged_patient_profile {} {} PASSED ".format(item['id'],item['fullName']))
        except:
            is_all_pass &= False
            
            if count==0:
                util.print_fail_message("\ntest_post_discharged_patient_profile {} {} FAILED".format(item['id'],item['fullName']))
            else:
                util.print_fail_message("test_post_discharged_patient_profile {} {} FAILED".format(item['id'],item['fullName']))

        count+=1
    
    assert is_all_pass == True