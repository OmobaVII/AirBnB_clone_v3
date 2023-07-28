#!/usr/bin/python3
"""my api application"""
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """closes the storage for the session"""
    storage.close()


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, int(port), threaded=True)
