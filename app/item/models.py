from app.extensions import db
from sqlalchemy.orm import relationship, backref


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.GUID(), primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    category = db.Column(db.String(255))
    product_code = db.Column(db.String(255))
    modified_by = db.Column(db.GUID())
    modified_on = db.Column(db.DateTime)
    created_by = db.Column(db.GUID())
    created_at = db.Column(db.DateTime)

    def __getitem__(self, item):
        return getattr(self, item)


class Variant(db.Model):
    __tablename__ = 'variant'
    id = db.Column(db.GUID(), primary_key=True)
    item_id = db.Column(db.GUID(), db.ForeignKey('item.id', ondelete='CASCADE'))
    name = db.Column(db.String(255))
    selling_price = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)
    size = db.Column(db.String(255))
    cloth = db.Column(db.String(255))
    item = relationship(Item, backref=backref('variants', passive_deletes=True))
    modified_by = db.Column(db.GUID())
    modified_on = db.Column(db.DateTime)
    created_by = db.Column(db.GUID())
    created_at = db.Column(db.DateTime)

    def __getitem__(self, item):
        return getattr(self, item)


class UpdateTransactionLog(db.Model):
    __tablename__ = 'update_transaction_log'
    id = db.Column(db.GUID(), primary_key=True)
    item_id = db.Column(db.GUID(), db.ForeignKey('item.id', ondelete='CASCADE'))
    attribute = db.Column(db.String(255))
    old_value = db.Column(db.String(255))
    new_value = db.Column(db.String(255))
    entity_type = db.Column(db.String(255))  # item or variant
    update_type = db.Column(db.String(255))  # update or insert
    transaction_id = db.Column(db.Integer)
    item = relationship(Item)
    user_id = db.Column(db.GUID())
    modified_by = db.Column(db.GUID())
    modified_on = db.Column(db.DateTime)
    created_by = db.Column(db.GUID())
    created_at = db.Column(db.DateTime)

    def __getitem__(self, item):
        return getattr(self, item)