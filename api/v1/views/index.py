#!/usr/bin/python3
''' index file'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status():
    """ Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    ''' count all stats'''
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    dict = {}
    i = 0
    for value in classes.values():
        dict[names[i]] = storage.count(value)
        i += 1
    return jsonify(dict)
