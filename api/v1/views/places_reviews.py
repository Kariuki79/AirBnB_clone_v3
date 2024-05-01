#!/usr/bin/python3
"""Handles all default RESTFul API actions for Review objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response({}, 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    if 'user_id' not in request_data:
        abort(400, description='Missing user_id')
    if 'text' not in request_data:
        abort(400, description='Missing text')

    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    request_data['place_id'] = place_id
    new_review = Review(**request_data)
    storage.new(new_review)
    storage.save()
    return make_response(new_review.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_data = request.get_json()
    for key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
        request_data.pop(key, None)

    for key, value in request_data.items():
        setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
