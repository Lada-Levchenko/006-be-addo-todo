from flask import Blueprint, request, jsonify, g
from flask_login import login_required

from schemas import user_schema
from models import User

crud_user = Blueprint('crud_user', __name__)


@crud_user.route('', methods=["POST"])
def create():
    user, errors = user_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    user.save()

    return jsonify(user_schema.dump(user).data), 201


@crud_user.route('', methods=["GET"])
@login_required
def read_one():
    try:
        user = User.get(id=g.user.get_id())
        return jsonify(user_schema.dump(user).data)
    except User.DoesNotExist:
        return jsonify({"message": "Can't find user with id - `{id}`".format(id=g.user.get_id())}), 404


@crud_user.route('', methods=["PUT"])
@login_required
def update():
    try:
        user = User.get(id=g.user.get_id())
    except User.DoesNotExist:
        return jsonify({"message": "Can't find user with id - `{id}`".format(id=g.user.get_id())}), 404

    user, errors = user_schema.load(request.json, instance=user)

    if errors:
        return jsonify(errors), 400

    user.save()

    return jsonify(user_schema.dumps(user).data), 200


@crud_user.route('', methods=["DELETE"])
@login_required
def delete():
    User.delete().where(User.id == g.user.get_id()).execute()
    return jsonify({}), 204
