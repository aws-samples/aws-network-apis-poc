'''
This module contains all the functions related to the Telco.
'''
import requests
import json
from dotenv import load_dotenv
import os

class Telco():
    '''
    The Telco class is used to interact with the Telco QoD APIs.
    '''
    def __init__(self):
        '''
        Initializes a Telco object.
        '''
        load_dotenv(".env")
        # General Deliverables
        self.domain_name = os.environ['DOMAIN_NAME']

        # Specific Deliverables
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.x_subject_name = os.environ['X_SUBJECT_NAME']

    def generate_qod_access_token(self):
        '''
        Generate an Access Token.
        '''
        url = f'https://{self.domain_name}/oauth/client_credential/accesstoken?grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        r = requests.post(url=url, headers=headers, data=data)
        self.log_request(r)
        return r.json()['access_token']

    def create_qod_session(self, data):
        '''
        Create a QoD Session.
        '''
        access_token = self.generate_qod_access_token()
        url = f'https://{self.domain_name}/hp3v-meccontroller-v1-qos/sessions'
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.client_id,
            'X-SUBJECT-NAME': self.x_subject_name,
            'X-CLIENT-CERT-STATUS': 'ok',
            'Authorization': f'Bearer {access_token}'
        }
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        self.log_request(r)

        if r.status_code == 200:
            return {"id": r.json()["sessionId"]}

        return None

    def get_qod_session(self, session_id):
        '''
        Get a QoD Session.
        '''
        access_token = self.generate_qod_access_token()
        url = f'https://{self.domain_name}/hp3v-meccontroller-v1-qos/sessions/{session_id}'
        headers = {
            'apikey': self.client_id,
            'X-SUBJECT-NAME': self.x_subject_name,
            'X-CLIENT-CERT-STATUS': 'ok',
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
        url = f'https://{self.domain_name}/hp3v-meccontroller-v1-qos/sessions/{session_id}'
        headers = {
            'apikey': self.client_id,
            'X-SUBJECT-NAME': self.x_subject_name,
            'X-CLIENT-CERT-STATUS': 'ok',
            'Authorization': f'Bearer {access_token}'
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
