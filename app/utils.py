import datetime
import hashlib
import uuid
from flask import jsonify
import json
from app.extensions import g
from app.user.models import Users
from app.user.serializers import UsersSchema
from app.item.models import Item
from app.item.serializers import ItemSchema, VariantSchema, UpdateTransactionLogSchema


def convert_list_to_dict(lst, key_name):
    obj = {}
    for i in lst:
        obj[i[key_name]] = i
    return obj


def hash_password(password):
    salt = "admin"
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password


def create(create_obj):
    uuid_id = uuid.uuid4()
    create_obj.id = uuid_id
    create_obj.created_at = datetime.datetime.now()
    g.session.add(create_obj)
    g.session.commit()
    g.session.flush()


def update(updated_object):
    entity = updated_object.__class__
    object_id = updated_object.id
    g.session.query(entity).filter_by(id=object_id).one()
    serialize_to_json(updated_object)
    updated_object.modified_on = datetime.datetime.now()
    g.session.merge(updated_object)
    g.session.commit()
    g.session.flush()
    entity = entity.__name__
    return updated_object


def delete(delete_obj):
    if delete_obj is not None:
        g.session.delete(delete_obj)
        delete_obj.modified_on = datetime.datetime.now()
        g.session.commit()
        g.session.flush()


def search_api(search_obj, entity):
    return fetch_list(entity, search_obj)


def bad_request(message, status_code):
    response = jsonify({'message': message})
    response.status_code = status_code
    return response


def bulk_create(obj_list, entity):
    list_obj = []
    for each_object in obj_list:
        if entity == Users:
            each_object["password"] = hash_password(each_object["password"])
        create_obj = entity(**each_object)
        uuid_id = uuid.uuid4()
        create_obj.id = uuid_id
        create_obj.created_at = datetime.datetime.now()
        create_obj.created_by = g.user.id if g.get('user') else None
        list_obj.append(create_obj)
    g.session.add_all(list_obj)
    g.session.commit()
    g.session.flush()
    return list_obj


def fetch_list(entity, constraint_list):
    object_list = g.session.query(entity).filter_by(**constraint_list).all()
    json_list = [serialize_to_json(i) for i in object_list]
    return json_list


def fetch(entity, constraint_list):
    obj = g.session.query(entity).filter_by(**constraint_list).first()
    if obj:
        obj = serialize_to_json(obj)
    return obj


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def serialize_to_json(entity):
    entity_name = entity.__class__.__name__
    entity_serializer = entity_name + 'Schema'
    entity_serializer = eval(entity_serializer)()
    return json.loads(entity_serializer.dumps(entity, cls=UUIDEncoder).data)
