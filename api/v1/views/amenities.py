#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
all default RESTFul API actions"""
from flask import jsonify, abort, request
from flasgger.utils import swag_from
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml', methods=['GET'])
def get_amenities():
    """Get all Amenities"""
    return jsonify([amenity.to_dict() for amenity in storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """Get an Amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an Amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def create_amenity():
    """Create a new Amenity"""
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an Amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200

