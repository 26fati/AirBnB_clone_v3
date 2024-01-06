#!/usr/bin/python3
""" objects that handle all default RestFul API actions for places """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_city(city_id):
    """
    Retrieves the list of all places objects
    of a specific city, or a specific place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    lst = []
    for place in city.places:
        lst.append(place.to_dict())
    return jsonify(lst)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific place based on id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place based on id provided
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
    Creates a place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404, description="Missing user_id")
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_i"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
