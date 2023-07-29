#!/usr/bin/python3
"""view for link between Place and AMenity objects
handles all default RESTful API actions"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenites_by_place(place_id):
    """retrieves a list of all amenities of a place"""
    a_place = storage.get(Place, place_id)
    if a_place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenity_list = []
        for amenity in a_place.amenities:
            amenity_list.append(amenity.to_dict())
    else:
        amenity_list = [storage.get(Amenity, amenity_id).to_dict()
                        for amenity_id in a_place.amenity_ids]
    return jsonify(amenity_list)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """deletes an amenity attached to a place"""
    a_place = storage.get(Place, place_id)
    an_amenity = storage.get(Amenity, amenity_id)
    if a_place is None or an_amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if an_amenity not in a_place.amenities:
            abort(404)
        place.amenities.remove(an_amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(an_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """link an amenity to a place"""
    a_place = storage.get(Place, place_id)
    an_amenity = storage.get(Amenity, amenity_id)
    if a_place is None or an_amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if an_amenity in a_place.amenities:
            return jsonify(an_amenity.to_dict()), 200
        else:
            a_place.amenities.append(an_amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(an_amenity.to_dict()), 200
        else:
            a_place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(an_amenity.to_dict()), 201
