'''
This module contains all the functions related to the Telco.
'''
import requests
import json
import jwt
import time
from dotenv import load_dotenv
import os

API_VERSION_V0 = 'v0'
API_VERSION_V1 = 'v1'

class Telco():
    '''
    The Telco class is used to interact with the Telco QoD APIs.
    '''
    def __init__(self):
        '''
        Initializes a Telco object.
        '''
        load_dotenv(".env")
        # API Variables
        self.auth_domain_name = os.environ['AUTH_DOMAIN_NAME']
        self.api_domain_name = os.environ['API_DOMAIN_NAME']
        self.api_version = os.environ['API_VERSION']

        # AWS Specific Variables
        self.admin_app_secret = os.environ['ADMIN_APP_SECRET']
        self.path_to_private_pem = os.environ['PATH_TO_PRIVATE_PEM']
        self.path_to_public_pem =  os.environ['PATH_TO_PUBLIC_PEM']
        self.issuer = os.environ['ISSUER']

        # App Developer Variables
        self.purpose = os.environ["PURPOSE"]
        self.app_secret = os.environ['APP_SECRET']

    def generate_qod_access_token(self):
        '''
        Generate an Access Token.
        '''
        url = f'https://{self.auth_domain_name}/bc-authorize'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.app_secret}'
        }
        data = {
            'login_hint_token': self.create_jwt(),
            'purpose': f'{self.purpose}'
        }
        r = requests.post(url=url, headers=headers, data=data)
        self.log_request(r)
        auth_req_id = r.json()['auth_req_id']

        # Generate Access Token using Authentication Request ID generated from CIBA Flow
        url = f'https://{self.auth_domain_name}/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.app_secret}'
        }
        data = {
            'grant_type': 'urn:openid:params:grant-type:ciba',
            'auth_req_id': auth_req_id
        }
        r = requests.post(url=url, headers=headers, data=data)
        self.log_request(r)
        return r.json()['access_token']

    def create_qod_session(self, data):
        '''
        Create a QoD Session.
        '''
        access_token = self.generate_qod_access_token()
        url = f'https://{self.api_domain_name}'
        if self.api_version == API_VERSION_V0:
            url = f'{url}/qod/v0/sessions'
        elif self.api_version == API_VERSION_V1:
            url = f'{url}/qod-rc/v1/sessions'
        else:
            raise Exception(f"API VERSION is not valid {self.api_version}.")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        self.log_request(r)

        if r.status_code == 201:
            if self.api_version == API_VERSION_V0:
                return {"id": r.json()["id"]}
            elif self.api_version == API_VERSION_V1:
                return {"session_id": r.json()["id"]}

        return None

    def get_qod_session(self, session_id):
        '''
        Get a QoD Session.
        '''
        access_token = self.generate_qod_access_token()
        url = f'https://{self.api_domain_name}'
        if self.api_version == API_VERSION_V0:
            url = f'{url}/qod/v0/sessions'
        elif self.api_version == API_VERSION_V1:
            url = f'{url}/qod-rc/v1/sessions'
        else:
            raise Exception(f"API VERSION is not valid {self.api_version}.")
        url = f'{url}/{session_id}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.get(url=url, headers=headers)
        self.log_request(r)
        return r.json()

    def delete_qod_session(self, session_id):
        '''
        Delete a QoD Session.
        '''
        access_token = self.generate_qod_access_token()
        url = f'https://{self.api_domain_name}'
        if self.api_version == API_VERSION_V0:
            url = f'{url}/qod/v0/sessions'
        elif self.api_version == API_VERSION_V1:
            url = f'{url}/qod-rc/v1/sessions'
        else:
            raise Exception(f"API VERSION is not valid {self.api_version}.")
        url = f'{url}/{session_id}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.delete(url=url, headers=headers)
        self.log_request(r)
        return

    def generate_purpose_access_token(self):
        '''
        Generate an Access Token.
        '''
        # Generate Access Token to create a Purpose
        url = f'https://{self.auth_domain_name}/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.admin_app_secret}'
        }
        data = {
            'scope': 'gdpr:purposes:create gdpr:purposes:read', # gdpr:purposes:delete',
            'grant_type': 'client_credentials'
        }
        r = requests.post(url=url, headers=headers, data=data)
        self.log_request(r)
        return r.json()['access_token']

    def create_purpose(self, purpose_data):
        # Create a Purpose
        access_token = self.generate_purpose_access_token()
        url = f'https://{self.api_domain_name}/gdpr/v1/purposes'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.post(url=url, headers=headers, data=json.dumps(purpose_data))
        self.log_request(r)

        if r.status_code == 201:
            return {"id": r.json()["id"]}
        
        return r.json()

    def get_purpose(self, purpose_id):
        '''
        Get a Purpose.
        '''
        # Generate Access Token
        access_token = self.generate_purpose_access_token()
        url = f'https://{self.api_domain_name}/gdpr/v1/purposes/{purpose_id}'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.get(url=url, headers=headers)
        self.log_request(r)
        return r.json()

    def delete_purpose(self, purpose_id):
        '''
        Delete a Purpose.
        '''
        # Generate Access Token
        access_token = self.generate_purpose_access_token()
        url = f'https://{self.api_domain_name}/gdpr/v1/purposes/{purpose_id}'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.delete(url=url, headers=headers)
        self.log_request(r)
        return r.json()

    def generate_apps_access_token(self):
        '''
        Generate an Access Token.
        '''
        url = f'https://{self.auth_domain_name}/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.admin_app_secret}'
        }
        data = {
            'scope': 'admin:apps:create admin:apps:read admin:apps:delete',
            'grant_type': 'client_credentials'
        }
        r = requests.post(url=url, headers=headers, data=data)
        self.log_request(r)
        return r.json()['access_token']

    def create_app(self, app_data):
        # Generate Access Token
        access_token = self.generate_apps_access_token()

        # Create App
        url = f'https://{self.api_domain_name}/admin/v2/apps'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.post(url=url, headers=headers, data=json.dumps(app_data))
        self.log_request(r)
        
        if r.status_code == 201:
            return {"id": r.json()["id"]}
        
        return r.json()

    def get_app(self, app_id):
        '''
        Get a App.
        '''
        # Generate Access Token
        access_token = self.generate_apps_access_token()
        url = f'https://{self.api_domain_name}/admin/v2/apps/{app_id}'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.get(url=url, headers=headers)
        self.log_request(r)
        return r.json()

    def delete_app(self, app_id):
        '''
        Delete a App.
        '''
        # Generate Access Token
        access_token = self.generate_apps_access_token()
        url = f'https://{self.api_domain_name}/admin/v2/apps/{app_id}'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.delete(url=url, headers=headers)
        self.log_request(r)
        return r.json()

    # TODO: Hardcoded to use Phone Number temporarily until IP is supported.
    def create_jwt(self):
        with open(self.path_to_private_pem, 'r') as f:
            private_key = f.read()

        headers = {
            "alg": "RS256",
            "typ": "JWT"
        }
        payload = {
            "aud": f"https://{self.auth_domain_name}/",
            "iss": f"{self.issuer}",
            "exp": int(time.time()) + 10000,
            "iat": int(time.time()),
            # identifier_type is either phone_number or ip
            "identifier_type": "phone_number",
            # identifier is either UE phone number or ip
            "identifier": "+34696836198"
        }
        encoded = jwt.encode(payload=payload, key=private_key, algorithm="RS256", headers=headers)

        with open(self.path_to_public_pem, 'r') as fi:
            public_key = fi.read()
        decoded = jwt.decode(encoded, public_key, algorithms=["RS256"], audience=f"https://{self.auth_domain_name}/")

        # DEBUG
        print()
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        print(f"Encoded JWT: {encoded}")
        print(f"Decoded JWT: {decoded}")
        print()

        return encoded

    def log_request(self, r):
        print()
        print(f"Request:")
        print(f"URL: {r.request.url}")
        print(f"Headers: {r.request.headers}")
        print(f"Body: {r.request.body}")
        print()
        print(f"Response:")
        print(f"URL: {r.url}")
        print(f"Headers: {r.headers}")
        print(f"Body: {r.text}")
        print()
        return
