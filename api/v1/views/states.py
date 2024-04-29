#!/usr/bin/python3
"""Handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage, state

@app_views.route("/states", strict_slashes=False)
def get_states():
    """retrieves the list of all state objects"""
    all_states = storage.all("State").values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)

@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """Retrives a state object by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Deletes a state object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def post_states():
    """Creates a state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    results = request.get_json()
    instance = state(**results)
    instance.save()
    return make_response(jsonify(instance.to_dict(), 201))

@app_views.route("/state/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    results = request.get_json()
    if results is None:
        abort(400, "Not a JSON")
    else:
        for key, value in results.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
        storage.save()
        data = state.to_dict()
        return make_response(jsonify(data), 200)



    

        




