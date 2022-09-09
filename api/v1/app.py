#!/usr/bin/python3
"""
Start web aptication
"""
from api.v1.views import app_views
from models import storage
from flask import Flask
import os


host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '500')
app = Flask(__name____)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close():
    """
    Close session
    """
    storage.close()


if __name__ == "__main__":
    """
    Start api
    """
    app.run(host=host, port=port, threaded=True)
