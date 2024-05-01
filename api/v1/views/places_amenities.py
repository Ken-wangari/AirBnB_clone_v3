#!/usr/bin/python3
"""New view for the link between Place objects and Amenity objects"""
from os import getenv
from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flasgger.utils import swag_from

mode = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml', methods=['GET'])
def get_place_amenities(place_id):
    """Get all amenities of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if mode == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict() for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Delete an Amenity object from a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201

