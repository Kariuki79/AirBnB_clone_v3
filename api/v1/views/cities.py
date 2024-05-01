#!/usr/bin/python3
"""Handles all default RESTFul API actions for City objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, description='Missing name')

    request_data['state_id'] = state_id
    new_city = City(**request_data)
    storage.new(new_city)
    storage.save()
    return make_response(new_city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    for key in ['id', 'state_id', 'created_at', 'updated_at']:
        request_data.pop(key, None)

    for key, value in request_data.items():
        setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
