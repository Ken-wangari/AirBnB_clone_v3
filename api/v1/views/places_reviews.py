#!/usr/bin/python3
"""This module implements Flask routes for managing reviews"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flasgger.utils import swag_from


def get_place_or_404(place_id):
    """Get place by ID or return 404 if not found"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return place


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieve reviews associated with a specific place"""
    place = get_place_or_404(place_id)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review(review_id):
    """Retrieve a specific review by its ID"""
    review = storage.get(Review, review_id)
    return jsonify(review.to_dict()) if review else abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """Delete a specific review by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def create_review(place_id):
    """Create a new review associated with a specific place"""
    place = get_place_or_404(place_id)
    req_json = request.get_json()
    if not req_json or 'user_id' not in req_json or 'text' not in req_json:
        abort(400, description="Invalid JSON or missing user_id/text")
    user = storage.get(User, req_json['user_id'])
    if not user:
        abort(404)
    new_review = Review(**req_json)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def update_review(review_id):
    """Update an existing review by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        abort(400, description="Invalid JSON")
    for key, value in req_json.items():
        if key not in ("id", "user_id", "place_id", "created_at", "updated_at"):
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

