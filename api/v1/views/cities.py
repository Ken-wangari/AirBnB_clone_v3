#!/usr/bin/python3
"""This module implements rules for handling City objects"""
from flask import jsonify, abort, request
from flasgger.utils import swag_from
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities_by_state(state_id):
    """Get cities by state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """Get a city by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def create_city(state_id):
    """Create a new city in a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    data["state_id"] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def update_city(city_id):
    """Update a city by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

