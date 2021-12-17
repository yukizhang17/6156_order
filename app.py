import flask
from flask import *
from application_services.order_service import *
import json
from flask_cors import CORS
from middleware import notification

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
        oid = insert_order(request.json)
        if oid == "Failed":
            return "The order couldn't been created", 400
        res = {"location": f"/orders/{oid}"}
        notification.notify(flask.request)
        return json.dumps(res), 201


@app.route('/orders/<orderID>', methods=['GET', 'POST'])
def order_id(orderID):
    if flask.request.method == 'GET':
        res = get_order_by_oid(orderID)
        if len(res) == 0:
            return "Cannot find resource.", 404
        return json.dumps(res, default=str), 200

    elif flask.request.method == 'POST':
        update_order_status(orderID, request.json)
        return f"Order {orderID}'s status has been updated", 200


@app.route('/orders/user/<userID>', methods=['GET'])
def orders_by_user_id(userID):
    """
    Function to get orders by uid
    """
    # form = flask.request.json
    offset = None
    limit = None
    # for element in form:
    #     if element == "limit":
    #         limit = form[element]
    #     elif element == "offset":
    #         offset = form[element]
    return json.dumps(get_order_by_uid(userID, limit, offset), default=str), 200


@app.route('/orders/business/<businessID>', methods=['GET'])
def orders_by_business_id(businessID):
    """
    Function to get orders by bid
    """

    # form = flask.request.json
    offset = None
    limit = None

    # for element in form:
    #     if element == "limit":
    #         limit = form[element]
    #     elif element == "offset":
    #         offset = form[element]

    return json.dumps(get_order_by_bid(businessID, limit, offset), default=str), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')