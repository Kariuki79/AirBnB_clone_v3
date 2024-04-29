#!/usr/bin/python3
"""Handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    """Retrieves the list of all state objects"""
    all_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_method_state(state_id):
    """Retrieves a state object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_method(state_id):
    """ delete state object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_obj():
    """ creating a state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = State(**js)
    obj.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_method(state_id):
    """ updates a state object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
