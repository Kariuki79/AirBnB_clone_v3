#!/usr/bin/python3
"""Handles all crud RESTFul API actions"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage, user


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all("User").values()
    list_users = [user_obj.to_dict() for user_obj in all_users]
    return jsonify(list_users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by id"""
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    new_user = user.User(**request.json)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)
    storage.save()
    return jsonify(user_obj.to_dict()), 200
