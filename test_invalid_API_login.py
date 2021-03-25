from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login as login
import data.url_extension as url_ext
import util

# verify that error thrown when email is invalid during sign in
# store accessToken in global variable
def test_post_sign_in_invalid_email():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SIGN_IN)
    client = ServerApi(api_url=API_URL)
    response = client.post_without_bearer_token(
                            {
                                "email": "invalid_email",
                                "emailVerifier": login.EMAILVERIFIER,
                                "domain": login.DOMAIN
                            }
                        )
    assert response.status_code == 401
    assert response.json()['title'] == 'Unauthorized'
    assert response.json()['type'] == 'https://tools.ietf.org/html/rfc7235#section-3.1'

# verify that error thrown when email verifier is invalid during sign in
# store accessToken in global variable
def test_post_sign_in_invalid_email_verifier():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SIGN_IN)
    client = ServerApi(api_url=API_URL)
    response = client.post_without_bearer_token(
                            {
                                "email": login.EMAIL,
                                "emailVerifier": "invalid email verifier",
                                "domain": login.DOMAIN
                            }
                        )
    assert response.status_code == 500

# verify that error thrown when domain is invalid during sign in
# store accessToken in global variable
def test_post_sign_in_invalid_domain():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SIGN_IN)
    client = ServerApi(api_url=API_URL)
    response = client.post_without_bearer_token(
                            {
                                "email": login.EMAIL,
                                "emailVerifier": login.EMAILVERIFIER,
                                "domain": "invalid domain"
                            }
                        )
    print(response.json())
    assert response.status_code == 400
    assert response.json()['errors']['domain'] == ['Error converting value "invalid domain" to type \'OneRehab.Services.Operations.Messages.Identity.DomainGroup\'. Path \'domain\', line 1, position 413.']
    assert response.json()['type'] == 'https://tools.ietf.org/html/rfc7231#section-6.5.1'
    assert response.json()['title'] == 'One or more validation errors occurred.'
    