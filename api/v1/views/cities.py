#!/usr/bin/python3
""" objects that handle all default RestFul API actions for cities """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_state(state_id):
    """
    Retrieves the list of all cities objects
    of a specific State, or a specific city
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    lst = []
    for city in state.cities:
        lst.append(city.to_dict())
    return jsonify(lst)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_cities(city_id):
    """
    Retrieves a specific city based on id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a city based on id provided
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
