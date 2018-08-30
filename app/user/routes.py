from flask import jsonify
from flask import Blueprint
from flask import request, abort
from controller import (create_user_ctrl, get_user_list_ctrl, get_user_by_id_ctrl,
                        get_user_by_mail_ctrl, delete_user_ctrl, update_user_ctrl,
                        search_user_ctrl)
from app.token.controller import get_token_ctrl
from models import Users
from app.utils import fetch

user_api = Blueprint('user_api', __name__)


@user_api.route('/user', methods=['POST'])
def create_user():
    req_data = request.json
    token_obj = {'email': req_data['email'], 'password': req_data['password']}
    user_email = req_data['email']
    if fetch(Users, {'email': user_email}) is None:
        create_user_ctrl(req_data)
        return jsonify(get_token_ctrl(token_obj))
    else:
        return "Email_already_exist"
# try:
# except Exception as ex:
#     abort(400, {'message': str(ex)})


@user_api.route('/user', methods=['GET'])
def get_user_list():
    try:
        return jsonify(get_user_list_ctrl())
    except Exception as ex:
        abort(400, {'message': str(ex)})


@user_api.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        return jsonify(get_user_by_id_ctrl(user_id))
    except Exception as ex:
        abort(400, {'message': str(ex)})


@user_api.route('/user/mailauth/<user_mail_id>', methods=['GET'])
def get_user_by_mail(user_mail_id):
    try:
        return jsonify(get_user_by_mail_ctrl(user_mail_id))
    except Exception as ex:
        abort(400, {'message': str(ex)})


@user_api.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        return delete_user_ctrl(user_id)
    except Exception as ex:
        abort(400, {'message': str(ex)})


@user_api.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        obj = request.json
        return jsonify(update_user_ctrl(obj, user_id))
    except Exception as ex:
        abort(400, {'message': str(ex)})


@user_api.route('/user/search', methods=['POST'])
def search_user():
    try:
        return jsonify(search_user_ctrl(request.json))
    except Exception as ex:
        abort(400, {'message': str(ex)})
