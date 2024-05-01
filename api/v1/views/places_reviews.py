#!/usr/bin/python3
"""This module implements rules for handling Review objects"""
from flask import jsonify, abort, request
from flasgger.utils import swag_from
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_reviews_by_place(place_id):
    """Get Review objects by Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review(review_id):
    """Get a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def create_review(place_id):
    """Insert a Review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def update_review(review_id):
    """Update a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

