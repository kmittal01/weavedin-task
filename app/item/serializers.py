from marshmallow_sqlalchemy import ModelSchema
from models import Item, Variant, UpdateTransactionLog


class ItemSchema(ModelSchema):
    class Meta:
        model = Item


class VariantSchema(ModelSchema):
    class Meta:
        model = Variant


class UpdateTransactionLogSchema(ModelSchema):
    class Meta:
        model = UpdateTransactionLog
