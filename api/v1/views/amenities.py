#!/usr/bin/python3
""" objects that handle all default RestFul API actions for cities """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenities
    """
    lst = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        dic = amenity.to_dict()
        lst.append(dic)
    return jsonify(lst)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves a specific State """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenty_by_id(amenity_id):
    """
    Deletes a State Object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenities():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=["PUT"], strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """
    Updates a State
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
