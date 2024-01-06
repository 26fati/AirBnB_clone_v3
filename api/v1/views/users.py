#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def get_users():
    """
    Retrieves the list of all Users Objects
    """
    lst = []
    users = storage.all(User)
    for user in users.values():
        dic = user.to_dict()
        lst.append(dic)
    return jsonify(lst)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves a specific User """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Deletes a User Object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a User
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    
    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def update_user_by_id(user_id):
    """
    Updates a User
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
