#!/usr/bin/python3
"""This module implements Flask routes for managing places"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flasgger.utils import swag_from


def get_object_or_404(model, obj_id):
    """Helper function to get an object by ID or return 404"""
    obj = storage.get(model, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieve places associated with a specific city"""
    city = get_object_or_404(City, city_id)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific place by its ID"""
    place = get_object_or_404(Place, place_id)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """Delete a specific place by its ID"""
    place = get_object_or_404(Place, place_id)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def create_place(city_id):
    """Create a new place associated with a specific city"""
    city = get_object_or_404(City, city_id)
    req_json = request.get_json()
    if not req_json or 'user_id' not in req_json or 'name' not in req_json:
        abort(400, description="Invalid JSON or missing user_id/name")
    user = get_object_or_404(User, req_json['user_id'])
    new_place = Place(**req_json)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def search_places():
    """Search places based on specified criteria"""
    req_json = request.get_json()
    if not isinstance(req_json, dict):
        abort(400, description="Invalid JSON")
    
    states = [get_object_or_404(State, state_id) for state_id in req_json.get('states', [])]
    cities = [city for state in states for city in state.cities] + [get_object_or_404(City, city_id) for city_id in req_json.get('cities', [])]
    amenities = [get_object_or_404(Amenity, amenity_id) for amenity_id in req_json.get('amenities', [])]

    places = [place for city in cities for place in city.places]

    result_places = []
    for place in places:
        if all(amenity in place.amenities for amenity in amenities):
            result_places.append(place.to_dict())

    return jsonify(result_places)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def update_place(place_id):
    """Update an existing place by its ID"""
    place = get_object_or_404(Place, place_id)
    req_json = request.get_json()
    if not isinstance(req_json, dict):
        abort(400, description="Invalid JSON")

    for key, value in req_json.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

