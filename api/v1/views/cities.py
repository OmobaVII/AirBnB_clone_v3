#!/usr/bin/python3
"""new view for city objects that handles
default RESTful API actions"""
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """retrives the list of all city objects in a state"""
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)
    city_list = []
    for city in a_state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cityid(city_id):
    """return a city corresponding the id"""
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)

    return jsonify(a_city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city corresponding the id"""
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    a_city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """creates a new city"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        a_state = storage.get(State, state_id)
        if a_state is None:
            abort(404)
        new_city = City(**data)
        new_city.state_id = a_state.id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        a_city.name = data['name']
        a_city.save()

        return jsonify(a_city.to_dict()), 200
