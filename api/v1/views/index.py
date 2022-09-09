#!/usr/bin/python3
"""
Init methods
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """
    Return if the app is working
    """
    return jsonify({"status": "OK"})


@app_views.route('/status')
def num_obj_bytype():
    """ endpoint that retrieves the number of each objects by type """
    return jsonify({
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    })
