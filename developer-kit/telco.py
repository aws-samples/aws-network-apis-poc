'''
This module contains all the functions related to the Telco.
'''
import requests
import json
import os
from dotenv import load_dotenv

class Telco():
    '''
    The Telco class is used to interact with the Telco QoD APIs.
    '''
    def __init__(self):
        '''
        Initializes a Telco object.
        '''
        load_dotenv(".env")
        self.domain_name = os.environ["DOMAIN_NAME"]
        self.client_id = os.environ["CLIENT_ID"]
        self.client_secret = os.environ["CLIENT_SECRET"]
        self.scope = os.environ["SCOPE"]
        self.access_token = self.generate_access_token()

    def parse_create_qod_session_data(self, data):
        '''
        Parse the input data object to the expected QOD Session Data API input
        '''
        # QoS Configuration
        config = {}

        # duration
        duration = data.get("duration")
        if duration is not None:
            config["duration"] = duration

        # ueId
        ueId = data.get("ueId")
        if ueId is not None:
            config["ueId"] = ueId

        # asId
        asId = data.get("asId")
        if asId is not None:
            config["asId"] = asId

        # uePorts
        uePorts = data.get("uePorts")
        if uePorts is not None:
            config["uePorts"] = uePorts

        # asPorts
        asPorts = data.get("asPorts")
        if asPorts is not None:
            config["asPorts"] = asPorts

        # qos
        qos = data.get("qos")
        if qos is not None:
            config["qos"] = qos

        return config

    def generate_access_token(self):
        '''
        Generate an Access Token.
        '''
        url = f'https://{self.domain_name}/oauth2/token'
        headers = {
            'Host': f'{self.domain_name}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': f'{self.client_id}',
            'client_secret': f'{self.client_secret}',
            'scope': f'{self.scope}',
        }
        r = requests.post(url=url, headers=headers, data=data)
        self.log_request(r)
        return r.json()['access_token']

    def create_qod_session(self, data):
        '''
        Create a QoD Session.
        '''
        url = f'https://{self.domain_name}/qod/v0/sessions'
        headers = {
            'Host': f'{self.domain_name}',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        data = self.parse_create_qod_session_data(data)
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        self.log_request(r)

        if r.status_code == 201:
            return {"id": r.json()["id"]}
        return None

    def get_qod_session(self, session_id):
        '''
        Get a QoD Session.
        '''
        url = f'https://{self.domain_name}/qod/v0/sessions/{session_id}'
        headers = {
            'Host': f'{self.domain_name}',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        r = requests.get(url=url, headers=headers)
        self.log_request(r)
        return r.json()

    def delete_qod_session(self, session_id):
        '''
        Delete a QoD Session.
        '''
        url = f'https://{self.domain_name}/qod/v0/sessions/{session_id}'
        headers = {
            'Host': f'{self.domain_name}',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        r = requests.delete(url=url, headers=headers)
        self.log_request(r)
        return

    def log_request(self, r):
        print()
        print(f"URL: {r.request.url}")
        print(f"Headers: {r.request.headers}")
        print(f"Body: {r.request.body}")
        print(f"Response: {r.text}")
        print()
        return
