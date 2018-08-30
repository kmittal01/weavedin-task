import requests
import json
from utils import random_string_generator, staticValues


class TestUser(object):

    def test_user_insert(self):
        url = staticValues.base_url + '/user'
        headers = {
            'authorization': "",
            'content-type': "application/json",
        }
        payload = {
            "name": "Kshitij",
            "email": "admin{0}@weavedin.com".format(random_string_generator()),
            "password": "admin123"
        }
        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)
        data = response.json()
        staticValues.user_obj = data['user']
        staticValues.user_id = data['user']['id']
        staticValues.user_password = payload['password']
        assert response.status_code == 200

    def test_token(self):
        url = staticValues.base_url + '/auth'
        headers = {
            'authorization': "",
            'content-type': "application/json",
        }
        payload = {
            "email": staticValues.user_obj['email'],
            "password": staticValues.user_password
        }
        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)
        staticValues.token = response.json()['token']
        assert response.status_code == 200
