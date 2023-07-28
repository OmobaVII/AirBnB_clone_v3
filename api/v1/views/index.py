#!/usr/bin/python3
"""the index file of my views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status of the API"""
    return jsonify({"status": "OK"})
