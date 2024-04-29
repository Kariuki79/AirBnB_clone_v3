#!/usr/bin/python3
"""Handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage, state


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all state objects"""
    all_states = storage.all("State").values()
    list_states = [state_obj.to_dict() for state_obj in all_states]
    return jsonify(list_states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state object by id"""
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object"""
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    new_state = state.State(**request.json)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state"""
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
