#!/usr/bin/python3
"""
Start web aptication
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close():
    """
    Close session
    """
    storage.close()


@app.errorhandler(404)
def error_notfound(error):
    """ returns a JSON-formatted 404 status code response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """
    Start api
    """
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '500')
    app.run(host=host, port=port, threaded=True)
