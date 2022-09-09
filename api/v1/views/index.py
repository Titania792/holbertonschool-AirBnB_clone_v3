#!/usr/bin/python3
"""
Init methods
"""
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    """
    Return if the app is working
    """
    return jsonify({"status": "OK"})
