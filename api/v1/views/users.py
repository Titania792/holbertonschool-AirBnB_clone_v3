#!/usr/bin/python3
""" new view for user objects that handles all default RESTFul API actions """

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """
    if request.method == 'GET':
        users = []
        for user in storage.all(User).values():
            users.append(user.to_dict())
        return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user(user_id):
    """ Retrieves a user object """
    if request.method == 'GET':
        if storage.get(User, user_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user object """
    if request.method == 'DELETE':
        if storage.get(user, user_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(User, user_id))
            storage.save()
            return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    """ Creates a user """
    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            return jsonify({"error": "Not a JSON"}), 400
        elif 'email' not in req:
            return jsonify({"error": "Missing email"}), 400
        elif 'password' not in req:
            return jsonify({"error": "Missing password"}), 400
        new_user = User(**req)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            return jsonify({"error": "Not a JSON"}), 400
        if storage.get(User, user_id) is None:
            abort(404)
        else:
            if 'password' in req:
                storage.get(User, user_id).password = req['password']
            if 'first_name' in req:
                storage.get(User, user_id).first_name = req['first_name']
            if 'last_name' in req:
                storage.get(User, user_id).last_name = req['last_name']
            storage.get(user, user_id).save()
            return jsonify(storage.get(User, user_id).to_dict()), 200
