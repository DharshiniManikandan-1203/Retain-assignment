from flask import Blueprint, request
from app import models
from app.utils import json_response

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return json_response(message="User Management API is running!")

@bp.route('/users', methods=['GET'])
def get_all_users():
    return json_response(models.get_all_users())

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = models.get_user(user_id)
    return json_response(user) if user else json_response(message="User not found", status=404)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(k in data for k in ('name', 'email', 'password')):
        return json_response(message="Missing fields", status=400)

    models.create_user(data['name'], data['email'], data['password'])
    return json_response(message="User created successfully", status=201)

@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not all(k in data for k in ('name', 'email')):
        return json_response(message="Missing fields", status=400)

    models.update_user(user_id, data['name'], data['email'])
    return json_response(message="User updated successfully")

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    models.delete_user(user_id)
    return json_response(message="User deleted successfully")

@bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return json_response(message="Please provide a name", status=400)

    return json_response(models.search_users(name))

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = models.login_user(data['email'], data['password'])
    if user_id:
        return json_response({"user_id": user_id}, message="Login successful")
    return json_response(message="Invalid credentials", status=401)
