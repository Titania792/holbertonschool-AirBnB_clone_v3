#!/usr/bin/python3
""" new view for review objects that handles all default
RESTFul API actions """

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """ Retrieves the list of all review objects """
    if request.method == 'GET':
        if storage.get(Place, place_id) is None:
            abort(404)
        all_reviews = storage.all(Review).values()
        reviews = []
        for review in all_reviews:
            if review.place_id == place_id:
                reviews.append(review.to_dict())
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review(review_id):
    """ Retrieves a review object """
    if request.method == 'GET':
        if storage.get(Review, review_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review object """
    if storage.get(Review, review_id) is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(storage.get(Review, review_id))
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    """ Creates a review """
    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            return jsonify({"error": "Not a JSON"}), 400
        elif 'user_id' not in req:
            return jsonify({"error": "Missing user_id"}), 400
        elif 'text' not in req:
            return jsonify({"error": "Missing text"}), 400
        if storage.get(User, req['user_id']) is None:
            abort(404)
        if storage.get(Place, place_id) is None:
            abort(404)
        else:
            req['place_id'] = place_id
            new_review = Review(**req)
            new_review.save()
            return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a review object """
    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            return jsonify({"error": "Not a JSON"}), 400
        if storage.get(Review, review_id) is None:
            abort(404)
        else:
            if 'text' in req:
                storage.get(Review, review_id).text = req['text']
            storage.get(Review, review_id).save()
            return jsonify(storage.get(Review, review_id).to_dict()), 200
