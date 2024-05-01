#!/usr/bin/python3
"""
This module implements a Flask web application for an AirBnB clone RESTful API
"""
from flask import Flask, jsonify
import models
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def view_status():
    """Returns the status of the application"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def view_stats():
    """Retrieves the number of each object by type"""
    model_counts = {
        "amenities": models.storage.count(models.Amenity),
        "cities": models.storage.count(models.City),
        "places": models.storage.count(models.Place),
        "reviews": models.storage.count(models.Review),
        "states": models.storage.count(models.State),
        "users": models.storage.count(models.User)
    }
    return jsonify(model_counts)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the current SQLAlchemy Session"""
    models.storage.close()


@app.errorhandler(404)
def handle_404_error(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = "0.0.0.0"
    port = 5000
    app.run(host=host, port=port, threaded=True)

