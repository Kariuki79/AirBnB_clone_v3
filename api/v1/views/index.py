#!/usr/bin/python3
"""index module"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """Return status ok"""
    return jsonify({'status': 'ok'})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """Defines stats route"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})