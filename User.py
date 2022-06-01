from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from model import User, Order, Session
from shm import UserSchema
from flask_httpauth import HTTPBasicAuth

user = Blueprint('user', __name__)
bcrypt = Bcrypt()

session = Session()
auth = HTTPBasicAuth()

# Password Verification
@auth.verify_password
def verify_password(login, password):
    try:
        user = session.query(User).filter_by(login=login).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return login
    except:
        return None

# Register new user
@user.route('/api/v1/User', methods=['POST'])
def register():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    exists = session.query(User).filter_by(login=data['login']).first()
    if exists:
        return Response(status=404, response='User with such login already exists.')

    # Hash user's password
    hashed_password = bcrypt.generate_password_hash(data['password'])
    # Create new user
    new_user = User(firstName=data['firstName'], lastName=data['lastName'], email=data['email'], phone=data['phone'], login=data['login'], password=hashed_password, is_provisor=data['is_provisor'])

    # Add new user to db
    session.add(new_user)
    session.commit()

    return Response(response='New user was successfully created!')


# Get user by id
@user.route('/api/v1/getuser/<id_user>', methods=['GET'])
#@auth.login_required
def get_user(id_user):
    # Check if user exists
    db_user = session.query(User).filter_by(id_user=id_user).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')
    if db_user.login != auth.username():
        return Response(status=404, response='You can get only your information')

    # Return user data
    user_data = {'id': db_user.id_user, 'name': db_user.firstName, 'surname': db_user.lastName}
    return jsonify({"user": user_data})

# Update user by id
@user.route('/api/v1/updateuser/<id_user>', methods=['PUT'])
#@auth.login_required
def update_user(id_user):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user exists
    db_user = session.query(User).filter_by(id_user=id_user).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')
    if db_user.login != auth.username():
        return Response(status=404, response='You can update only your information')

    # Check if login is not taken if user tries to change it
    if 'login' in data.keys():
        exists = session.query(User).filter_by(login=data['login']).first()
        if exists:
            return Response(status=400, response='User with such login already exists.')
        db_user.login = data['login']
    # Change user data
    if 'firstName' in data.keys():
        db_user.firstName = data['firstName']
    if "lastName" in data.keys():
        db_user.lastName = data['lastName']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        db_user.password = hashed_password
    if "email" in data.keys():
        db_user.email = data['email']
    if "phone" in data.keys():
        db_user.phone = data['phone']
    if "is_provisor" in data.keys():
        db_user.is_provisor = data['is_provisor']
    # Save changes
    session.commit()

    # Return new user data
    user_data = {'id': db_user.id_user, 'firstName': db_user.firstName, 'lastName': db_user.lastName}
    return jsonify({"user": user_data})


# Delete user by id
@user.route('/api/v1/deleteuser/<id_user>', methods=['DELETE'])
#@auth.login_required
def delete_user(id_user):
    # Check if user exists
    db_user = session.query(User).filter_by(id_user=id_user).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')
    if db_user.login != auth.username():
        return Response(status=404, response='You can delete only your account')
    db_order = session.query(Order).filter_by(id_user=id_user).first()
    if not db_order:
        # Delete user
        session.delete(db_user)
        session.commit()
        return Response(response='User was deleted.')
    else:
        return Response(status=400, response='User already has orders.')
