import uuid
from application_services.base_application_resource import BaseApplicationResource
import datetime

DB = "orders"
TABLE = "user_product"


def get_all_order():
    return BaseApplicationResource.get_by_template(DB, TABLE, None)


def get_order_by_oid(order_id):
    template = {"oid": order_id}
    return BaseApplicationResource.get_by_template(DB, TABLE, template)


def get_order_by_uid(user_id, limit, offset):
    template = {"uid": user_id}
    return BaseApplicationResource.get_by_template(DB, TABLE, template, limit, offset)


def get_order_by_bid(business_id, limit, offset):
    template = {"bid": business_id}
    return BaseApplicationResource.get_by_template(DB, TABLE, template, limit, offset)


def insert_order(create_data):
    """
    Function to insert new order entry by admin
    """
    oid = uuid.uuid4().hex
    template = {"oid": oid}
    for item in create_data:
        template[item] = create_data[item]
    try:
        BaseApplicationResource.create(DB, TABLE, template)
        return oid
    except:
        return "Failed"


def insert_order_by_uid(uid, create_data):
    """
    Function to insert new order entry by user
    """
    template = {"uid": uid}
    for item in create_data:
        template[item] = create_data[item]
    try:
        BaseApplicationResource.create(DB, TABLE, template)
        return "Done"
    except:
        return "Failed"


def update_order_status(orderID, update_data):
    update_data['timestamp'] = datetime.now()
    template = {'oid': orderID}
    BaseApplicationResource.update(DB, TABLE, update_data, template)
