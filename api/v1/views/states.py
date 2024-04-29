#!/usr/bin/python3
"""Handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    """Retrieves the list of all state objects"""
    all_objs = []

    for state in storage.all("State").values():
        all_objs.append(state.to_dict())

    return jsonify(all_objs)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_method_state(state_id):
    """Retrieves a state object by id"""
    all_states = storage.all("State")

    for state in all_states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_method(state_id):
    """ delete state object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_obj():
    """ creating a n"""
    if not request.get_json():
        abort(400, description='Not a JSON')

    request_body = request.get_json()

    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    new_state = State(**request_body)
    storage.new(new_state)
    storage.save()
    return make_response(new_state.to_dict(), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def post_method(state_id):
    """ post method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
