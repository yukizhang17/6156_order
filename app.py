import flask
from flask import *
from application_services.order_service import *
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index_page():
    return "This is the order's homepage.", 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    """
    Function to query all orders from DB or insert new orders
    by admin
    """
    # Or return all data entries from table
    if flask.request.method == 'GET':
        return json.dumps(get_all_order(), default=str), 200

    else:
        oid = insert_order(request.form)
        if oid == "Failed":
            return "The order couldn't been created", 400
        res = {"location": f"/users/{oid}"}
        return json.dumps(res), 201


@app.route('/orders/<orderID>', methods=['GET', 'POST'])
def order_id(orderID):
    if flask.request.method == 'GET':
        res = get_order_by_oid(orderID)
        if len(res) == 0:
            return "Cannot find resource.", 404
        return json.dumps(res, default=str), 200

    elif flask.request.method == 'POST':
        update_order_status(orderID, request.form)
        return f"Order {orderID}'s status has been updated", 200


@app.route('/orders/user/<userID>', methods=['GET'])
def orders_by_user_id(userID):
    """
    Function to get orders by uid
    """
    return json.dumps(get_order_by_uid(userID), default=str), 200


@app.route('/orders/business/<businessID>', methods=['GET'])
def orders_by_business_id(businessID):
    """
    Function to get orders by bid
    """
    return json.dumps(get_order_by_bid(businessID), default=str), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)