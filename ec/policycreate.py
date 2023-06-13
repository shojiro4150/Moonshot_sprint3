import requests
from .local_settings import *

def create_session_and_login():
    
    # Create a session with Socotra
    session = requests.Session()
    response = session.post(
        'https://api.sandbox.socotra.com/account/authenticate',
        json={'username': username,
              'password': password,
              'hostName': hostname})

    # Save the authorization token for use in future requests
    authorization_token = response.json()['authorizationToken']
    session.headers.update({'Authorization': authorization_token})
    return session
