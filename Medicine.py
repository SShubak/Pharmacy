from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from pymysql import Date

from model import Medicine, Session, Order, User, Medicine, Session
from shm import MedicineSchema
from User import auth

medicine = Blueprint('medicine', __name__)
bcrypt = Bcrypt()

session = Session()


# Register new medicine
@medicine.route('/api/v1/Medicine', methods=['POST'])
@auth.verify_password
def register():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        MedicineSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if medicine already exists
    exists = session.query(Medicine).filter_by(name=data['name']).first()
    if exists:
        return Response(status=400, response='Medicine with such name already exists.')
    db_user = session.query(User).filter_by(login=auth.username()).first()
    if db_user.is_provisor != 1:
        return Response(status=404, response='Provisor Only')
    # Create new medicine
    new_medicine = Medicine(name=data['name'], manufacturer=data['manufacturer'], price=data['price'], in_stock=True,
                            demand=False, in_stock_number=data['in_stock_number'], demand_number=0)

    # Add new medicine to db
    session.add(new_medicine)
    session.commit()

    return Response(response='New medicine was successfully created!')


# Get all medicines
@medicine.route('/api/v1/allMedicine', methods=['GET'])
@auth.verify_password
def get_reservations():
    # Get all medicines from db
    medicines = session.query(Medicine)

    if not medicines:
        return Response(status=404, response='No one medicine')
    db_user = session.query(User).filter_by(login=auth.username()).first()

    # Return all medicines
    output = []
    for r in medicines:
        output.append({'id_medicine': r.id_medicine,
                       'name': r.name,
                       'price': r.price,
                       'manufacturer': r.manufacturer,
                       'in_stock_number': r.in_stock_number})
    return jsonify(output)


# Get medicine by id
@medicine.route('/api/v1/getmedicine/<id_medicine>', methods=['GET'])
@auth.verify_password
def get_user(id_medicine):
    # Check if medicine exists
    session2 = Session()
    db_medicine = session2.query(Medicine).filter_by(id_medicine=id_medicine).first()
    print("hereeeeeeeeee")
    if not db_medicine:
        return Response(status=404, response='Medicine with provided ID was not found.')

    # Return medicine data
    medicine_data = {'name': db_medicine.name, 'price': db_medicine.price}
    return jsonify(medicine_data), 200


# Update medicine by id
@medicine.route('/api/v1/medicine/<id_medicine>', methods=['PUT'])
@auth.verify_password
def update_user(id_medicine):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        MedicineSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if medicine exists
    db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
    if not db_medicine:
        return Response(status=404, response='Medicine with provided ID was not found.')
    db_user = session.query(User).filter_by(login=auth.username()).first()
    if db_user.is_provisor != 1:
        return Response(status=404, response='Provisor Only')

    # Check if medicine name is not taken if name already exists
    if 'name' in data.keys():
        exists = session.query(Medicine).filter_by(name=data['name']).first()
        if exists:
            return Response(status=400, response='Medicine with such name already exists.')
        db_medicine.name = data['name']
    # Change medicine data
    if 'name' in data.keys():
        db_medicine.name = data['name']
    if 'manufacturer' in data.keys():
        db_medicine.manufacturer = data['manufacturer']
    if 'price' in data.keys():
        db_medicine.price = data['price']
    if 'in_stock' in data.keys():
        db_medicine.in_stock = data['in_stock']
    if 'demand' in data.keys():
        db_medicine.demand = data['demand']
    if 'in_stock_number' in data.keys():
        db_medicine.in_stock_number = data['in_stock_number']
    if 'demand_number' in data.keys():
        db_medicine.demand_number = data['demand_number']

    # Save changes
    session.commit()

    # Return new medicine data
    medicine_data = {'id': db_medicine.id_medicine, 'name': db_medicine.name, 'surname': db_medicine.price}
    return jsonify({"medicine": medicine_data})


# Delete medicine by id
@medicine.route('/api/v1/medicine/<id_medicine>', methods=['DELETE'])
@auth.verify_password
def delete_user(id_medicine):
    # Check if medicine exists
    db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
    if not db_medicine:
        return Response(status=404, response='Medicine with provided ID was not found.')
    db_user = session.query(User).filter_by(login=auth.username()).first()
    if db_user.is_provisor != 1:
        return Response(status=404, response='Provisor Only')

    # Delete medicine
    session.delete(db_medicine)
    session.commit()
    return Response(response='Medicine was deleted.')
