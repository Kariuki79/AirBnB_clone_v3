#!/usr/bin/python3
"""Handles all default RESTFul API actions for User objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response({}, 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    if 'email' not in request_data:
        abort(400, description='Missing email')
    if 'password' not in request_data:
        abort(400, description='Missing password')

    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return make_response(new_user.to_dict(), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    for key in ['id', 'email', 'created_at', 'updated_at']:
        request_data.pop(key, None)

    for key, value in request_data.items():
        setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
