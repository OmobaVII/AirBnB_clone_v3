#!/usr/bin/python3
"""my api application"""
from flask import Flask, make_response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origines="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """closes the storage for the session"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """handlers for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, int(port), threaded=True)
