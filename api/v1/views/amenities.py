#!/usr/bin/python3
"""Handles all default RESTFul API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = ([amenity.to_dict() for amenity in storage.all(Amenity).
                  values()])
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, description='Missing name')

    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()
    return make_response(new_amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    for key in ['id', 'created_at', 'updated_at']:
        request_data.pop(key, None)

    for key, value in request_data.items():
        setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
