#!/usr/bin/env python3

from flask import Flask, jsonify
from models import storage
from models.base_model import State, User, Amenity, City, Place, Review

app = Flask(__name__)


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    return jsonify(status='OK')


@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    models = {'states': State, 'users': User, 'amenities': Amenity,
              'cities': City, 'places': Place, 'reviews': Review}

    stats = {key: storage.count(value) for key, value in models.items()}

    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)

