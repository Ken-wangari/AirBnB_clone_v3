#!/usr/bin/python3
"""
This script starts a Flask web application for an AirBnB clone RESTful API
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from models import storage
from api.v1.views import app_views

# Initialize Flask application
app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views)

# Enable CORS for all routes under /api/v1
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

# Define Swagger configuration
app.config['SWAGGER'] = {
    'title': 'AirBnB Clone RESTful API',
    'uiversion': 3
}

# Initialize Swagger
Swagger(app)


# Define teardown function to close SQLAlchemy Session
@app.teardown_appcontext
def teardown(error):
    """Closes the current SQLAlchemy Session"""
    storage.close()


# Define error handler for 404 errors
@app.errorhandler(404)
def handle_404_error(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    # Retrieve host and port from environment variables or use defaults
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

    # Run the Flask application
    app.run(host=host, port=port, threaded=True)

