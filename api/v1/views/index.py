#!/usr/bin/python3
"""
Init methods
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
    Return if the app is working
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def num_obj_bytype():
    """ endpoint that retrieves the number of each objects by type """
    dic = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(dic)
