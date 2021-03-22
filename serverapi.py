import requests
import data.login_uat as login

class ServerApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def post_without_bearer_token(self, payload=None):
        api_url = self.api_url
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        return requests.post(api_url, json=payload, headers=headers, verify=False)

    def post_with_bearer_token(self, payload=None):
        api_url = self.api_url
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Authorization": "Bearer {}".format(login.ACCESS_TOKEN)
        }
        return requests.post(api_url, json=payload, headers=headers, verify=False)

    def get_with_bearer_token(self, payload=None):
        api_url = self.api_url
        headers = {
           "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Authorization": "Bearer {}".format(login.ACCESS_TOKEN)
        }
        return requests.get(api_url, json=payload, headers=headers, verify=False)