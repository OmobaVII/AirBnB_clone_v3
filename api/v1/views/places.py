#!/usr/bin/python3
"""new view for place objects that handles
default RESTful API actions"""
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    """retrives the list of all places objects in a city"""
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    place_list = []
    for place in a_city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_placeid(place_id):
    """return a place corresponding the id"""
    a_place = storage.get(Place, place_id)
    if a_place is None:
        abort(404)

    return jsonify(a_place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place corresponding the id"""
    a_place = storage.get(Place, place_id)
    if a_place is None:
        abort(404)
    a_place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """creates a new place"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    else:
        data = request.get_json()
        a_user = storage.get(User, data['user_id'])
        a_city = storage.get(City, city_id)
        if a_city is None or a_user is None:
            abort(404)
        data['city_id'] = a_city.id
        data['user_id'] = a_user.id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place"""
    a_place = storage.get(Place, place_id)
    if a_place is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        keys_ignore = ("id", "user_id", "created_at", "updated_at")
        for key, val in data.items():
            if key in keys_ignore:
                pass
            else:
                setattr(a_place, key, val)
        a_place.save()

        return jsonify(a_place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)    
