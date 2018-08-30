from models import Item, Variant, UpdateTransactionLog
from app.utils import create, update, serialize_to_json
from app.extensions import g


def create_item_ctrl(obj):
    item = Item(**obj)
    create(item)
    return serialize_to_json(item)


def create_item_variant_ctrl(item_id, obj):
    obj['item_id'] = item_id
    variant = Variant(**obj)
    create(variant)
    return serialize_to_json(variant)


def update_transaction_log(user_id, obj, entity_type, update_type):
    last_transaction = g.session.query(UpdateTransactionLog).filter_by(user_id=user_id).order_by(
        UpdateTransactionLog.transaction_id.desc()).all()
    if last_transaction and len(last_transaction) > 0:
        last_transaction_id = last_transaction[0].transaction_id
    else:
        last_transaction_id = 0
    new_transaction_id = last_transaction_id + 1
    if entity_type == "variant":
        last_obj = g.session.query(Variant).filter_by(id=obj["id"]).all()[0]
        item_id = last_obj["item_id"]
    elif entity_type == "item":
        last_obj = g.session.query(Item).filter_by(id=obj["id"]).all()[0]
        item_id = last_obj["id"]
    else:
        return  # Error should be handled here.
    for attribute in obj:
        tran_log = UpdateTransactionLog(**{
            "attribute": attribute,
            "old_value": last_obj[attribute],
            "new_value": obj[attribute],
            "user_id": user_id,
            "entity_type": entity_type,
            "update_type": update_type,
            "transaction_id": new_transaction_id,
            "item_id": item_id
        })
        create(tran_log)
        serialize_to_json(tran_log)
        return serialize_to_json(tran_log)


def update_item_variant_ctrl(variant_id, obj):
    obj['id'] = variant_id
    update_transaction_log(g.user.id, obj, "variant", "update")
    variant = Variant(**obj)
    variant = update(variant)
    return serialize_to_json(variant)


def update_item_ctrl(item_id, obj):
    obj['id'] = item_id
    update_transaction_log(g.user.id, obj, "item", "update")
    item = Item(**obj)
    item = update(item)
    return serialize_to_json(item)

