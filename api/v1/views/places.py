#!/usr/bin/python3
"""This module implements rules for handling Place objects"""
from flask import jsonify, abort, request
from flasgger.utils import swag_from
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places_by_city(city_id):
    """Get place objects by city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """Get a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def create_place(city_id):
    """Insert a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def search_places():
    """Search for places based on criteria"""
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    id_states = data.get("states", [])
    id_cities = data.get("cities", [])
    id_amenities = data.get("amenities", [])
    places = []

    if id_states == id_cities == []:
        places = storage.all(Place).values()
    else:
        states = [storage.get(State, _id) for _id in id_states if storage.get(State, _id)]
        cities = [city for state in states for city in state.cities]
        cities += [storage.get(City, _id) for _id in id_cities if storage.get(City, _id)]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [storage.get(Amenity, _id) for _id in id_amenities if storage.get(Amenity, _id)]

    filtered_places = []
    for place in places:
        if all(amenity in place.amenities for amenity in amenities):
            filtered_places.append(place.to_dict())

    return jsonify(filtered_places)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def update_place(place_id):
    """Update a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

