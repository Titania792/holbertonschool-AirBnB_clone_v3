#!/usr/bin/python3
"""State"""

from api.vi.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'])
def get__task():
    """Show States"""
    states = []
    for state in storage.all('State').values():
        states.append(storage.to_dict())
    return jsonify(states)

@app_views.route("/states/<string:state_id>", methods=['GET'])
def get__task_id(state_id):
    """Get id of a task"""
    state_arr = storage.get('State', state_id)
    if state_arr is None:
        abort(404)
    return jsonify(state_arr.to_dict())

@app_views.route("/states/<string:state_id>", methods=['DELETE'])
def get__task_delete(state_id):
    """Delete task"""
    state_arr = storage.get('State', state_id)
    if state_arr is None:
        abort(404)
    else:
        storage.delete(state_arr)
        storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=['POST'])
def set__task_POST():
    """Create a new object"""
    if not request.json:
        return jsonify({"Error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"Error": "Missing name"}), 400

    state__post = State(**request.get_json())
    state__post.save()
    return jsonify(state__post.to_dict()), 201

@app_views.route("/states/<string:state_id>", methods=['PUT'])
def set__task_PUT():
    """Create a new object"""
    state_arr = storage.get('State', state_id)
    if not request.json:
        return jsonify({"Error": "Not a JSON"}), 400
    if state_arr is None:
        abort(400)
    for key, value in request.get_json().items():
        setattr(state_arr, key, value)
    storage.save()
    return jsonify(state_arr.to_dict()), 200


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)