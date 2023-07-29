#!/usr/bin/python3
"""new view for aemnity objects that handles
default RESTful API actions"""
from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenity():
    """retrives the list of all amenity objects"""
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenityid(amenity_id):
    """return a amenity corresponding the id"""
    a_amenity = storage.get(Amenity, amenity_id)
    if a_amenity is None:
        abort(404)

    return jsonify(a_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a amenity corresponding the id"""
    a_amenity = storage.get(Amenity, amenity_id)
    if a_amenity is None:
        abort(404)
    a_amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """creates a new amenity"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        Amenity(**data).save()
        return jsonify(Amenity(**data).to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity"""
    a_amenity = storage.get(Amenity, amenity_id)
    if a_amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        a_amenity.name = data['name']
        a_amenity.save()

        return jsonify(a_amenity.to_dict()), 200
