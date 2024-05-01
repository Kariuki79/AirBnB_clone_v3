#!/usr/bin/python3
"""Handles all default RESTFul API actions for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response({}, 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    if 'user_id' not in request_data:
        abort(400, description='Missing user_id')
    if 'name' not in request_data:
        abort(400, description='Missing name')

    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    request_data['city_id'] = city_id
    new_place = Place(**request_data)
    storage.new(new_place)
    storage.save()
    return make_response(new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    for key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
        request_data.pop(key, None)

    for key, value in request_data.items():
        setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the
    JSON in the body of the request
    """

    if request.is_json() is None:
        abort(400, description="Not a JSON")

    results = request.get_json()

    if not results or all(not results.get(key)
                          for key in results.keys()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = json_body.get("states", [])
    cities = json_body.get("cities", [])
    amenities = json_body.get("amenities", [])

    # Filter places based on states and cities
    filtered_places = set()
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                filtered_places.update(city.places)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            filtered_places.update(city.places)

    # Filter places based on amenities
    if amenities:
        filtered_places = [place for place in filtered_places
                           if all(amenity_id in place.amenities
                                  for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in filtered_places])
