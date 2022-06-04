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
            return user
    except:
        return None


# Register new user
@user.route('/api/v1/User', methods=['POST'])
def register():
    # Get data from request body
    data = request.get_json()
    print(data)
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
    new_user = User(firstName=data['firstName'], lastName=data['lastName'],
                    login=data['login'], password=hashed_password)

    # Add new user to db
    session.add(new_user)
    session.commit()

    return jsonify("all was successfully"),200


# Get user by id
@user.route('/api/v1/getuser/', methods=['GET'])
@auth.verify_password
def get_user():
    auth_data = auth.get_auth()
    db_user = session.query(User).filter_by(login=auth_data['username']).first().__dict__
    del db_user['password'], db_user['_sa_instance_state']
    return jsonify({"user": db_user})


@user.route('/api/v1/User/logout', methods=['POST'])
@auth.verify_password
def logout():
    return jsonify('Successful logout'), 200


# Update user by id
@user.route('/api/v1/updateuser', methods=['PUT'])
@auth.verify_password
def update_user():
    # Get data from request body
    data = request.get_json()
    auth_data = auth.get_auth()

    # Check if user exists
    db_user = session.query(User).filter_by(login=auth_data['username']).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')
    if db_user.login != auth_data['username']:
        return Response(status=404, response='You can update only your information')

    # Change user data
    if 'firstName' in data.keys():
        db_user.firstName = data['firstName']
    if "lastName" in data.keys():
        db_user.lastName = data['lastName']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        db_user.password = hashed_password
    # Save changes
    session.commit()

    # Return new user data
    user_data = {'id': db_user.id_user, 'firstName': db_user.firstName, 'lastName': db_user.lastName}
    return jsonify({"user": user_data})


# Delete user by id
@user.route('/api/v1/deleteuser/<id_user>', methods=['DELETE'])
# @auth.login_required
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
