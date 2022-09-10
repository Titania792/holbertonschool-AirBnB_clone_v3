#!/usr/bin/python3
""" new view for City objects that handles all default RESTFul API actions """

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all City objects of a State """
    if request.method == 'GET':
        if storage.get(State, state_id) is None:
            abort(404)
        else:
            cities = []
            for city in storage.all(City).values():
                if city.state_id == state_id:
                    cities.append(city.to_dict())
            return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """ Retrieves a City object """
    if request.method == 'GET':
        if storage.get(City, city_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(City, city_id).to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    if request.method == 'DELETE':
        if storage.get(City, city_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(City, city_id))
            storage.save()
            return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """ Creates a City """
    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            return jsonify({"error": "Not a JSON"}), 400
        elif 'name' not in req:
            return jsonify({"error": "Missing name"}), 400
        if storage.get(State, state_id) is None:
            abort(404)
        else:
            new_city = City(**req)
            new_city.state_id = state_id
            new_city.save()
            return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            return jsonify({"error": "Not a JSON"}), 400
        if storage.get(City, city_id) is None:
            abort(404)
        else:
            if 'name' in req:
                storage.get(City, city_id).name = req['name']
                storage.get(City, city_id).save()
                return jsonify(storage.get(City, city_id).to_dict()), 200
