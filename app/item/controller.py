from models import Item, Variant, UpdateTransactionLog
from app.user.models import Users
from app.utils import create, update, serialize_to_json
from app.extensions import g


def create_item_ctrl(obj):
    item = Item(**obj)
    create(item)
    return serialize_to_json(item)


def create_item_variant_ctrl(item_id, obj):
    obj['item_id'] = item_id
    update_transaction_log(g.user.id, obj, "variant", "insert")
    variant = Variant(**obj)
    create(variant)
    return serialize_to_json(variant)


def get_last_transaction(user_id):
    last_transaction = g.session.query(UpdateTransactionLog).filter_by(user_id=user_id).order_by(
        UpdateTransactionLog.transaction_id.desc()).all()
    if last_transaction and len(last_transaction) > 0:
        last_transaction_id = last_transaction[0].transaction_id
    else:
        last_transaction_id = 0
    return last_transaction_id


def update_transaction_log(user_id, obj, entity_type, update_type, last_transaction_id=None):
    if not last_transaction_id:
        last_transaction_id = get_last_transaction(user_id)
    new_transaction_id = last_transaction_id + 1
    last_obj = None
    item_id = None
    if update_type == "update":
        if entity_type == "variant":
            last_obj = g.session.query(Variant).filter_by(id=obj["id"]).all()[0]
            item_id = last_obj["item_id"]
        elif entity_type == "item":
            last_obj = g.session.query(Item).filter_by(id=obj["id"]).all()[0]
            item_id = last_obj["id"]
    elif update_type == "insert":
        item_id = obj["item_id"]
        last_obj = None
    for attribute in obj:
        if attribute in ["size", "name", "cloth", "category", "cost_price", "selling_price"]:
            tran_log = UpdateTransactionLog(**{
                "attribute": attribute,
                "old_value": last_obj[attribute] if last_obj else None,
                "new_value": obj[attribute],
                "user_id": user_id,
                "entity_type": entity_type,
                "update_type": update_type,
                "transaction_id": new_transaction_id,
                "item_id": item_id
            })
            create(tran_log)
    return


def update_item_variant_ctrl(variant_id, obj, last_transaction_id=None):
    obj['id'] = variant_id
    update_transaction_log(g.user.id, obj, "variant", "update", last_transaction_id=last_transaction_id)
    variant = Variant(**obj)
    variant = update(variant)
    return serialize_to_json(variant)


def update_item_ctrl(item_id, obj, last_transaction_id=None):
    obj['id'] = item_id
    update_transaction_log(g.user.id, obj, "item", "update", last_transaction_id=last_transaction_id)
    item = Item(**obj)
    item = update(item)
    return serialize_to_json(item)


def update_multiple_items_ctrl(obj):
    last_transaction_id = get_last_transaction(g.user.id)
    for item_id in obj:
        if 'attributes' in obj[item_id]:
            update_item_ctrl(item_id, obj[item_id]['attributes'], last_transaction_id=last_transaction_id)
        if 'variants' in obj[item_id]:
            for variant_id in obj[item_id]["variants"]:
                update_item_variant_ctrl(variant_id, obj[item_id]['variants'][variant_id],
                                         last_transaction_id=last_transaction_id)
    return


def get_user_transactions_ctrl(user_id):
    user = g.session.query(Users).filter_by(id=user_id).all()[0]
    transaction_dict = {}
    transaction_notifications = {}
    all_user_transaction = g.session.query(UpdateTransactionLog).filter_by(user_id=user_id).order_by(
        UpdateTransactionLog.transaction_id.desc()).all()
    for transaction in all_user_transaction:
        if transaction.transaction_id not in transaction_dict:
            transaction_dict[transaction.transaction_id] = []
        transaction_dict[transaction.transaction_id].append(serialize_to_json(transaction))

    for transaction_id in transaction_dict:
        for transaction_part in transaction_dict[transaction_id]:
            event = 'edited' if transaction_part['update_type'] == 'update' else 'inserted'
            if event == 'inserted':
                notification = user.name + ' ' + event + ' ' + transaction_part['entity_type'] + ' with ' + \
                               transaction_part['attribute'] + ' as ' + transaction_part['new_value']
            elif event == 'edited':
                notification = user.name + ' ' + event + ' ' + transaction_part['entity_type'] + ' with ' + \
                               transaction_part['attribute'] + ' as ' + transaction_part['old_value'] + ' to ' + \
                               transaction_part['new_value']
            if transaction_part["transaction_id"] not in transaction_notifications:
                transaction_notifications[transaction_part["transaction_id"]] = []
            transaction_notifications[transaction_part["transaction_id"]].append(notification)
    # print transaction_notifications
    return transaction_notifications


def get_all_user_transactions_ctrl():
    user_notifications = {}
    all_users = g.session.query(Users).all()
    for user in all_users:
        user_id = str(user.id)
        user_notifications[user_id] = get_user_transactions_ctrl(user_id)

    print user_notifications
    return user_notifications
