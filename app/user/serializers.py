from marshmallow_sqlalchemy import ModelSchema
from models import Users


class UsersSchema(ModelSchema):
    class Meta:
        model = Users
