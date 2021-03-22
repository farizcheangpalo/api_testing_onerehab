from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login_uat as login
import data.url_extension as url_ext
import util

# verify that user can login
# store accessToken in global variable
def test_post_sign_in():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SIGN_IN)
    client = ServerApi(api_url=API_URL)
    response = client.post_without_bearer_token(
                            {
                                "email": login.EMAIL,
                                "emailVerifier": login.EMAILVERIFIER,
                                "domain": login.DOMAIN
                            }
                        )
    assert response.status_code == 200
    login.ACCESS_TOKEN = response.json()['accessToken']

# verify that organizations are correct after login
def test_post_organizations():
    API_URL = "{}/{}".format(login.API_URL,url_ext.ORGANIZATIONS)
    client = ServerApi(api_url=API_URL)
    details = util.get_details_after_login(login.EMAIL,login.DOMAIN)
    response = client.post_with_bearer_token(
                            {
                                "userId": details['userId']
                            }
                        )
    assert response.status_code == 200
    assert response.json()["subOrgResponse"][0]["name"] == details['subOrgResponseName']
    assert response.json()["subOrgResponse"][0]["code"] == details['subOrgResponseCode']
    assert response.json()["subOrgResponse"][0]["orgCenterResponse"][0]["name"] == details['orgCenterResponseName']
    assert response.json()["subOrgResponse"][0]["orgCenterResponse"][0]["code"] == details['orgCenterResponseCode']

# verify that organization centers are correct after login
def test_get_organization_centers():
    API_URL = "{}/{}".format(login.API_URL,url_ext.ORGANIZATION_CENTERS)
    client = ServerApi(api_url=API_URL)
    expected_response_json = util.read_json_file("data/json/response/organization_centers.json")
    response = client.get_with_bearer_token()

    assert response.status_code == 200
    assert response.json() == expected_response_json
    

# verify that active list is correct
def test_post_active_list():
    API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
    client = ServerApi(api_url=API_URL)
    request_json = util.read_json_file("data/json/request/active_list.json")

    details = util.get_details_after_login(login.EMAIL,login.DOMAIN)
    request_json['organization'] = details['orgCenterResponseCode']
    response = client.post_with_bearer_token(request_json)

    assert response.status_code == 200
    assert response.json()['totalRecords'] >= 0
    assert response.json()['currentPageNumber'] >= 0
    assert response.json()['totalPage'] >= 0

    print(util.get_all_active_list(response.json()['totalPage']))

# verify that discharged list is correct
def test_post_discharged_list():
    API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
    client = ServerApi(api_url=API_URL)
    request_json = util.read_json_file("data/json/request/discharged_list.json")

    details = util.get_details_after_login(login.EMAIL,login.DOMAIN)
    request_json['organization'] = details['orgCenterResponseCode']
    response = client.post_with_bearer_token(request_json)

    assert response.status_code == 200
    assert response.json()['totalRecords'] >= 0
    assert response.json()['currentPageNumber'] >= 0
    assert response.json()['totalPage'] >= 0

    print(util.get_all_discharged_list(response.json()['totalPage']))
    

    