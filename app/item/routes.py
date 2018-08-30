from flask import Blueprint
from flask import request
from controller import (create_item_ctrl, create_item_variant_ctrl, update_item_variant_ctrl,
                        update_item_ctrl, update_multiple_items_ctrl, get_user_transactions_ctrl,
                        get_all_user_transactions_ctrl)
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


@item_api.route('/item/<item_id>', methods=['PUT'])
def update_item(item_id):
    return jsonify(update_item_ctrl(item_id, request.json))


@item_api.route('/item', methods=['PUT'])
def update_multiple_items():
    return jsonify(update_multiple_items_ctrl(request.json))


@item_api.route('/user_transactions/<user_id>', methods=['GET'])
def get_user_transactions(user_id):
    return jsonify(get_user_transactions_ctrl(user_id))


@item_api.route('/user_transactions/', methods=['GET'])
def get_all_user_transactions():
    return jsonify(get_all_user_transactions_ctrl())
