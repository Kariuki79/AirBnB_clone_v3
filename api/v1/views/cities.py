#!/usr/bin/python3
"""
City module to handle City related operations.
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves a list of cities for a given state ID.

    Args:
        state_id (str): ID of the state to retrieve cities for.

    Returns:
        JSON: A JSON response containing the list of cities for the state.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a city by its ID.

    Args:
        city_id (str): ID of the city to retrieve.

    Returns:
        JSON: A JSON response containing the city information.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
    Deletes a city by its ID.

    Args:
        city_id (str): ID of the city to delete.

    Returns:
        JSON: An empty JSON response indicating success.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_obj_city(state_id):
    """
    Creates a new city associated with a state.

    Args:
        state_id (str): ID of the state to associate the new city with.

    Returns:
        JSON: A JSON response containing the newly created city information.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    js = request.get_json()
    obj = City(**js)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def post_city(city_id):
    """
    Updates a city by its ID.

    Args:
        city_id (str): ID of the city to update.

    Returns:
        JSON: A JSON response containing the updated city information.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
