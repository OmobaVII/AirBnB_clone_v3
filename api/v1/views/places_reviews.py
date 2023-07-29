#!/usr/bin/python3
"""new view for Review objects that handles
default RESTful API actions"""
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """retrives the list of all reviews objects of a place"""
    a_place = storage.get(Place, place_id)
    if a_place is None:
        abort(404)
    review_list = []
    for review in a_place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviewid(review_id):
    """return a review corresponding the id"""
    a_review = storage.get(Review, review_id)
    if a_review is None:
        abort(404)

    return jsonify(a_review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review corresponding the id"""
    a_review = storage.get(Review, review_id)
    if a_review is None:
        abort(404)
    a_review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """creates a new review"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    else:
        data = request.get_json()
        a_place = storage.get(Place, place_id)
        a_user = storage.get(User, request.get_json()["user_id"])
        if a_place is None or a_user is None:
            abort(404)
        data['place_id'] = a_place.id
        data['user_id'] = a_user.id
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review"""
    a_review = storage.get(Review, review_id)
    if a_review is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        keys_ignore = ("id", "user_id", "place_id", "created_at", "updated_at")
        for key, val in data.items():
            if key in keys_ignore:
                pass
            else:
                setattr(a_review, key, val)
        a_review.save()

        return jsonify(a_review.to_dict()), 200
