from flask import jsonify
from models import Users
from app.utils import (bulk_create, hash_password, create, fetch_list, fetch, delete, update,
                       search_api, serialize_to_json)
from app.extensions import g


def create_user_ctrl(obj):

    if isinstance(obj, list):
        json_list = bulk_create(obj, Users)
        json_list = [serialize_to_json(i) for i in json_list]
        return json_list
    else:
        password_unhash = obj["password"]
        obj["password"] = hash_password(password_unhash)
        user = Users(**obj)
        create(user)
        return serialize_to_json(user)


def get_user_list_ctrl():
    return fetch_list(Users, {})


def get_user_by_mail_ctrl(user_mail_id):
    obj = g.session.query(Users).filter_by(email=user_mail_id)
    json_list = [serialize_to_json(i) for i in obj]
    return json_list


def get_user_by_id_ctrl(user_id):
    return fetch(Users, {"id": user_id})


def delete_user_ctrl(user_id):
    user = g.session.query(Users).filter_by(id=user_id).one()
    delete(user)
    return jsonify({"result": True})


def update_user_ctrl(obj, user_id):
    user = Users(**obj)
    user = update(user)
    return serialize_to_json(user)


def search_user_ctrl(obj):
    search = obj.json
    user_list = search_api(search, Users)
    json_list = [serialize_to_json(i) for i in user_list]
    return json_list
