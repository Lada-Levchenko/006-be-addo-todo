from flask import Blueprint, request, jsonify
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
def read():
    users = list(User.select())
    return jsonify(user_schema.dump(users, many=True).data)


@crud_user.route('/<int:id>', methods=["GET"])
def read_one(id):
    try:
        user = User.get(id=id)
        return jsonify(user_schema.dump(user).data)
    except User.DoesNotExist:
        return jsonify({"message": "Can't find user with id - `{id}`".format(id=id)}), 404


@crud_user.route('/<int:id>', methods=["PUT"])
def update(id):
    try:
        user = User.get(id=id)
    except User.DoesNotExist:
        return jsonify({"message": "Can't find user with id - `{id}`".format(id=id)}), 404

    user, errors = user_schema.load(request.json, instance=user)

    if errors:
        return jsonify(errors), 400

    user.save()

    return jsonify(user_schema.dumps(user).data), 200


@crud_user.route('/<int:id>', methods=["DELETE"])
def delete(id):
    is_user_exists = User.select().filter(id=id).exists()

    if not is_user_exists:
        return jsonify({"message": "Can't find user with id - `{id}`".format(id=id)}), 404

    User.delete().where(User.id == id).execute()
    return jsonify({}), 204
