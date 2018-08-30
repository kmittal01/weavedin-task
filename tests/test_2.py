import requests
import json
from utils import staticValues, random_string_generator
import time


class TestItem(object):
    ts = time.time()
    start_time = ts - 3600
    end_time = ts + 3600

    def test_item_insert(self):
        url = staticValues.base_url + '/item'
        headers = {
            'authorization': "",
            'token': staticValues.token,
            'content-type': "application/json",
        }
        payload = {
            "name": "item{0}".format(random_string_generator()),
            "brand": "Levis",
            "category": "Jeans",
            "product_code": "1234ABCD"
        }
        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        staticValues.item_id = response.json()['id']

        assert response.status_code == 200

    def test_item_insert2(self):
        url = staticValues.base_url + '/item'
        headers = {
            'authorization': "",
            'token': staticValues.token,
            'content-type': "application/json",
        }
        payload = {
            "name": "item{0}".format(random_string_generator()),
            "brand": "GAP",
            "category": "Tee",
            "product_code": "123412ABCD"
        }
        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        staticValues.item_id2 = response.json()['id']
        assert response.status_code == 200

    def test_variant_insert(self):
        url = staticValues.base_url + '/item/' + staticValues.item_id + "/variant"
        headers = {
            'authorization': "",
            'token': staticValues.token,
            'content-type': "application/json",
        }
        payload = {
            "name": "variant{0}".format(random_string_generator()),
            "selling_price": 2500,
            "cost_price": 2000,
            "size": "L",
            "cloth": "Denim",
        }
        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        staticValues.variant_id = response.json()['id']
        assert response.status_code == 200

    def test_variant_insert2(self):
        url = staticValues.base_url + '/item/' + staticValues.item_id2 + "/variant"
        headers = {
            'authorization': "",
            'token': staticValues.token,
            'content-type': "application/json",
        }
        payload = {
            "name": "variant{0}".format(random_string_generator()),
            "selling_price": 1500,
            "cost_price": 500,
            "size": "XL",
            "cloth": "Mixed",
        }
        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        staticValues.variant_id2 = response.json()['id']
        assert response.status_code == 200

    def test_update_item_variant(self):
        url = staticValues.base_url + '/variant/' + staticValues.variant_id
        headers = {
            'authorization': "",
            'content-type': "application/json",
            'token': staticValues.token
        }

        payload = {
            "cloth": "Cotton"
        }

        response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)
        assert response.status_code == 200

    def test_item_variant(self):
        url = staticValues.base_url + '/item/' + staticValues.item_id
        headers = {
            'authorization': "",
            'content-type': "application/json",
            'token': staticValues.token
        }

        payload = {
            "category": "Shorts"
        }

        response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)
        assert response.status_code == 200

    def test_update_multiple_item_variant(self):
        url = staticValues.base_url + '/item'
        headers = {
            'authorization': "",
            'content-type': "application/json",
            'token': staticValues.token
        }

        payload = {
            staticValues.item_id: {
                'attributes': {'category': 'Long Tee'},
                'variants': {staticValues.variant_id2: {'size': 'XXXS'}}
            },
            staticValues.item_id2: {
                'attributes': {"category": 'Short Tee'},
                'variants': {staticValues.variant_id2: {'size': 'XXXL'}}
            }
        }

        response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)
        assert response.status_code == 200

    def test_get_user_transactions(self):
        url = staticValues.base_url + '/user_transactions/' + staticValues.user_id + '/' + str(self.start_time) + '/' + str(self.end_time)
        headers = {
            'authorization': "",
            'content-type': "application/json",
            'token': staticValues.token
        }

        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200

    def test_get_all_user_transactions(self):
        url = staticValues.base_url + '/user_transactions' + '/' + str(self.start_time) + '/' + str(self.end_time)
        headers = {
            'authorization': "",
            'content-type': "application/json",
            'token': staticValues.token
        }

        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200
