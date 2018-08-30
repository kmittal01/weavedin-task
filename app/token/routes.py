from flask import Blueprint, jsonify
from flask import request, abort
from controller import get_token_ctrl

token = Blueprint('token_api', __name__)

# Token #


@token.route('/auth', methods=['POST'])
def get_token():
    try:
        return jsonify(get_token_ctrl(request.json))
    except Exception as ex:
        abort(400, {'message': str(ex)})
