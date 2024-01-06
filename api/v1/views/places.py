#!/usr/bin/python3
"""Handles default RESTful API actions for Place objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a specific City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific Place object based on ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a specific Place object based on ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    required_keys = ['user_id', 'name']
    for key in required_keys:
        if key not in data:
            abort(400, description=f"Missing {key}")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()

    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
