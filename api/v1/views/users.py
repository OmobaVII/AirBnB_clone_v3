#!/usr/bin/python3
"""new view for user objects that handles
default RESTful API actions"""
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_user():
    """retrives the list of all user objects"""
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_userid(user_id):
    """return a user corresponding the id"""
    a_user = storage.get(User, user_id)
    if a_user is None:
        abort(404)

    return jsonify(a_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user corresponding the id"""
    a_user = storage.get(User, user_id)
    if a_user is None:
        abort(404)
    a_user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates a new user"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    else:
        data = request.get_json()
        User(**data).save()
        return jsonify(User(**data).to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a user"""
    a_user = storage.get(User, user_id)
    if a_user is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        keys_ignore = ("id", "email", "created_at", "updated_at")
        for keys in data.keys():
            if keys in keys_ignore:
                pass
            else:
                setattr(a_user, keys, data[keys])
        a_user.save()

        return jsonify(a_user.to_dict()), 200
