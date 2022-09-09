#!/usr/bin/python3
"""
Init Blueprint
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__,
                       url='/api/v1')
