from flask import Blueprint
from flask import request
from controller import create_item_ctrl, create_item_variant_ctrl, update_item_variant_ctrl
from flask import jsonify

item_api = Blueprint('item_api', __name__)


# COURSE #


@item_api.route('/item', methods=['POST'])
def create_item():
    return jsonify(create_item_ctrl(request.json))


@item_api.route('/item/<item_id>/variant', methods=['POST'])
def create_item_variant(item_id):
    return jsonify(create_item_variant_ctrl(item_id, request.json))


@item_api.route('/variant/<variant_id>', methods=['PUT'])
def update_item_variant(variant_id):
    return jsonify(update_item_variant_ctrl(variant_id, request.json))
