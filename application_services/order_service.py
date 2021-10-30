import uuid
from application_services.base_application_resource import BaseApplicationResource

DB = "orders"
TABLE = "user_product"

def get_all_order():
    return BaseApplicationResource.get_by_template(DB, TABLE, None)

def get_order_by_uid(user_id):
    template = {"uid": user_id}
    return BaseApplicationResource.get_by_template(DB, TABLE, template)

def insert_order(create_data):
    """
    Function to insert new order entry by admin
    """
    template = {}
    for item in create_data:
        template[item] = create_data[item]
    try:
        BaseApplicationResource.create(DB, TABLE, template)
        return "Done"
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

"""
def update_order_status(create_data):
    template = {'uid': create_data['uid'], 'pid': create_data['pid'],
            'timestamp': create_data['timestamp']}

"""
