#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from models.base_model import State, User, Amenity, City, Place, Review
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def return_status():
    '''return API status'''
    return jsonify(status='OK')

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def return_stats():
    '''return JSON statistics'''
    models = {'states': State, 'users': User, 'amenities': Amenity,
              'cities': City, 'places': Place, 'reviews': Review}
    stats = {key: storage.count(value) for key, value in models.items()}
    return jsonify(stats)

