from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login_uat as login
import data.url_extension as url_ext
import util

# verify that patients profile details are correct
def test_post_active_patient_profile():
    API_URL = "{}/{}".format(login.API_URL,url_ext.PROFILE)
    client = ServerApi(api_url=API_URL)
    for item in login.ACTIVE_LIST_ITEMS:
        response = client.post_with_bearer_token(
                        {
                            "patientId": item['id'],
                            "dateOfBirth": item['dateofBirth'].split("T")[0]
                        }
                    )
        assert response.status_code == 200
        assert response.json()['id'] == item['id']
        assert response.json()['nric'] == item['nric']
        assert response.json()['dateofBirth'] == item['dateofBirth']
        assert response.json()['fullName'] == item['fullName']
        assert response.json()['gender'] == item['gender']

def test_post_discharged_patient_profile():
    API_URL = "{}/{}".format(login.API_URL,url_ext.PROFILE)
    client = ServerApi(api_url=API_URL)
    for item in login.DISCHARGED_LIST_ITEMS:
        response = client.post_with_bearer_token(
                        {
                            "patientId": item['id'],
                            "dateOfBirth": item['dateofBirth'].split("T")[0]
                        }
                    )
        assert response.status_code == 200
        assert response.json()['id'] == item['id']
        assert response.json()['nric'] == item['nric']
        assert response.json()['dateofBirth'] == item['dateofBirth']
        assert response.json()['fullName'] == item['fullName']
        assert response.json()['gender'] == item['gender']
    