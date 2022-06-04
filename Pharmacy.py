from datetime import datetime

from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from marshmallow.fields import Date

from model import Order, User, Medicine, Session
from shm import OrderSchema
from User import auth

order = Blueprint('order', __name__)
bcrypt = Bcrypt()

session = Session()


# Register new order
@order.route('/api/v1/pharmacy/orders', methods=['POST'])
@auth.verify_password
def register():
    # Get data from request body
    data = request.get_json()
    data['shipDate'] = data['shipDate'][:10]

    db_medicine = session.query(Medicine).filter_by(id_medicine=data['id_medicine']).first()
    if not db_medicine:
        return Response(status=404, response='Medicine with provided ID was not found.')

    db_user = session.query(User).filter_by(id_user=data['id_user']).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')
    if db_user.login != auth.username():
        return Response(status=404, response='You can get order on yourself')

    db_medicine.in_stock_number = db_medicine.in_stock_number - data['amount']

    # Create new order
    new_order = Order(id_medicine=data['id_medicine'], id_user=data['id_user'], shipDate=data['shipDate'],
                      amount=data['amount'])

    # Add new order to db
    session.add(new_order)
    session.commit()

    return jsonify('New order was successfully created!'), 200


# Get all orders
@order.route('/api/v1/pharmacy/orders', methods=['GET'])
def get_orders():
    # Get all orders from db
    orders = session.query(Order)

    if not orders:
        return Response(status=404, response='No one order')

    # Return all orders
    output = []
    for r in orders:
        output.append({'id_medicine': r.id_medicine,
                       'id_user': r.id_user,
                       'shipDate': r.shipDate,
                       'status': r.status,
                       'amount': r.amount,
                       'complete': r.complete})
    return jsonify({"orders": output})


# Get order by id
@order.route('/api/v1/pharmacy/orderscheck/<id_order>', methods=['GET'])
@auth.verify_password
def get_order(id_order):
    # Check if order exists
    db_orders = session.query(Order).filter_by(id_order=id_order).first()
    if not db_orders:
        return Response(status=404, response='A order with provided ID was not found.')
    db_user = session.query(User).filter_by(id_user=db_orders.id_user).first()
    if db_user.login != auth.username():
        return Response(status=404, response='You can get only your information')

    # Return order data
    order_data = {
        'id_order': db_orders.id_order,
        'id_medicine': db_orders.id_medicine,
        'id_user': db_orders.id_user,
        'shipDate': db_orders.shipDate,
        'amount': db_orders.amount,
        'status': db_orders.status,
        'complete': db_orders.complete
    }
    return jsonify({"order": order_data})


# Get all orders for user with provided login
@order.route('/api/v1/pharmacy/user/ordersall/', methods=['GET'])
@auth.verify_password
def get_orders_by_username():
    login = auth.get_auth()['username']
    # Check if user exists
    user = session.query(User).filter_by(login=login).first()
    if not user:
        return Response(status=404, response='User with such login was not found.')
    if login != auth.username():
        return Response(status=404, response='You can get only your information')

    # Get all user's orders from db
    orders = session.query(Order).filter_by(id_user=user.id_user)

    # Return all orders
    output = []
    for r in orders:
        output.append({'id_medicine': r.id_medicine,
                       'id_user': r.id_user,
                       'shipDate': r.shipDate,
                       'amount': r.amount})
    return jsonify(output),200


# Update order by id
@order.route('/api/v1/pharmacy/ordersupdate/<id_order>', methods=['PUT'])
@auth.verify_password
def update_user(id_order):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        OrderSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if order exists
    db_order = session.query(Order).filter_by(id_order=id_order).first()
    if not db_order:
        return Response(status=404, response='Order with provided ID was not found.')
    db_user = session.query(User).filter_by(id_user=db_order.id_user).first()
    if db_user.login != auth.username():
        return Response(status=404, response='You can update only your information')

    # Change medicine data
    if 'id_medicine' in data.keys():
        db_order.id_medicine = data['id_medicine']
    if 'id_user' in data.keys():
        db_order.id_user = data['id_user']
    if 'shipDate' in data.keys():
        db_order.shipDate = data['shipDate']
    if 'amount' in data.keys():
        db_order.amount = data['amount']
    if 'status' in data.keys():
        db_order.status = data['status']
    if 'complete' in data.keys():
        db_order.complete = data['complete']

    # Save changes
    session.commit()

    # Return new order data
    order_data = {'id': db_order.id_medicine, 'id_user': db_order.id_user, 'shipDate': db_order.shipDate,
                  'amount': db_order.amount, 'status': db_order.status, 'complete': db_order.complete}
    return jsonify({"order": order_data})


# Delete order by id
@order.route('/api/v1/pharmacy/orders/<id_order>', methods=['DELETE'])
@auth.verify_password
def delete_order(id_order):
    # Check if order exists
    db_orders = session.query(Order).filter_by(id_order=id_order).first()
    if not db_orders:
        return Response(status=404, response='A order with provided ID was not found.')
    db_user = session.query(User).filter_by(id_user=db_orders.id_user).first()
    if db_user.login != auth.username():
        return Response(status=404, response='You can delete your information')

    # Delete order
    session.delete(db_orders)
    session.commit()
    return Response(response='Order was deleted.')
