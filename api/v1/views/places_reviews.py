#!/usr/bin/python3
"""Handles all default RESTFul API actions for reviews"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage, review, place, user


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    all_reviews = [review_obj.to_dict() for review_obj in place_obj.reviews]
    return jsonify(all_reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by id"""
    review_obj = storage.get("Review", review_id)
    if not review_obj:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review_obj = storage.get("Review", review_id)
    if not review_obj:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    user_obj = storage.get("User", request.json['user_id'])
    if not user_obj:
        abort(404)
    if 'text' not in request.json:
        abort(400, "Missing text")
    new_review = review.Review(place_id=place_id,
                               user_id=request.json['user_id'], **request.json)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>",
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review"""
    review_obj = storage.get("Review", review_id)
    if not review_obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
