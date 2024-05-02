#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """Retrieve all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_state(state_id):
    """Retrieve a specific State object by its ID"""
    state = get_object_or_404(State, state_id)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """Delete a specific State object by its ID"""
    state = get_object_or_404(State, state_id)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_state():
    """Create a new State object"""
    req_json = request.get_json()
    if not is_valid_json(req_json, ['name']):
        abort(400, {'message': 'Invalid JSON or missing name'})
    new_state = State(**req_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_state(state_id):
    """Update an existing State object by its ID"""
    state = get_object_or_404(State, state_id)
    req_json = request.get_json()
    if not is_valid_json(req_json):
        abort(400, {'message': 'Invalid JSON'})
    for key, value in req_json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


def get_object_or_404(model, obj_id):
    """Helper function to get an object by ID or return 404"""
    obj = storage.get(model, obj_id)
    if obj is None:
        abort(404)
    return obj


def is_valid_json(data, required_keys=None):
    """Check if data is a valid JSON dictionary and contains required keys"""
    if not isinstance(data, dict):
        return False
    if required_keys:
        for key in required_keys:
            if key not in data:
                return False
    return True

