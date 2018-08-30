import requests
import json
from utils import staticValues, random_string_generator


class TestItem(object):

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
