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

@app.route('/orders', methods=['GET', 'POST', 'PUT'])
def orders():
    """
    Function to query all orders from DB or insert new orders
    by admin
    """
    # Or return all data entries from table
    if flask.request.method == 'GET':
       # return Response(json.dumps(get_all_order()), status=200,
               #  mimetype='application/json')
       return json.dumps(get_all_order()), 200

    elif flask.request.method == 'PUT':
        update_order_status(request.form)
    else:
        res = insert_order(request.form)
        if res == 'Done':
            return "The order has been created", 201
        else:
            return "The order couldn't been created", 400

@app.route('/users/<userID>/orders', methods=['GET', 'POST'])
def users_id_product(userID):
    """
    Function to get orders by uid or insert new order by users
    """
    if flask.request.method == 'POST':
        # Insert an (uid, pid, bid, timestamp) to DB
        res = insert_order_by_uid(uid, request.form)
        if res == 'Done':
            return f"Order for user {userID} has been created!", 201
        else:
            return f"Order for user {userID} couldn't be created", 400
    elif flask.request.method == 'GET':
        return json.dumps(get_order_by_uid(userID)), 200

if __name__ == '__main__':
    app.run()
