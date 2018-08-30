from flask import abort
from app.user.models import Users
import jwt
from app.utils import hash_password, serialize_to_json
from app.extensions import g


def get_token_ctrl(obj):
    user = g.session.query(Users).filter_by(email=obj['email']).one()
    if hash_password(obj['password']) != user.password:
        abort(403)
    encoded = jwt.encode({'id': str(user.id)}, 'secret', algorithm='HS256')
    return {"token": encoded, "user": serialize_to_json(user)}


def decode_token_ctrl(token):
    decode = jwt.decode(str(token), 'secret', algorithms=['HS256'])
    try:
        user = g.session.query(Users).filter_by(id=decode['id']).one()
    except Exception as e:
        print e
    return user
