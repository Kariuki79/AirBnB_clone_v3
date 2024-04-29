#!/usr/bin/python3
"""Handles all default RESTFul API actions"""


from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage, place, city, user


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    all_places = [place_obj.to_dict() for place_obj in city_obj.places]
    return jsonify(all_places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by id"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    user_obj = storage.get("User", request.json['user_id'])
    if not user_obj:
        abort(404)
    if 'name' not in request.json:
        abort(400, "Missing name")
    new_place = (place.Place(city_id=city_id, user_id=request.json['user_id'],
                             **request.json))
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict()), 200
