#!/usr/bin/python3
"""new view for state objects that handles
default RESTful API actions"""
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_state():
    """retrives the list of all State objects"""
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_stateid(state_id):
    """return a state corresponding the id"""
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)

    return jsonify(a_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state corresponding the id"""
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)
    a_state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a new state"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        State(**data).save()
        return jsonify(State(**data).to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state"""
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        a_state.name = data['name']
        a_state.save()

        return jsonify(a_state.to_dict()), 200
