#!/usr/bin/python3
"""city view that handles all default RESTFul API"""

from models.state import state
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, abort, make_response, request

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all city objects"""
    cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)

@app_views.route('/cities/<city_id>/', strict_slashes=False)
def get_city(city_id):
    """Retrieve a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a city"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities = request.get_json()
    if not cities:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in cities:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        cities['state_id'] = state.id
        city = City(**cities)
        city.save()
        
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """"updates a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    cities = request.get_json()
    if not cities:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        for key, value in cities.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
    return make_response(jsonify(city.to_dict()), 200)
