#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    lst = []
    states = storage.all(State)
    for state in states.values():
        dic = state.to_dict()
        lst.append(dic)
    return jsonify(lst)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Deletes a State Object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_states():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a valid JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Updates a State
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a valid JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
