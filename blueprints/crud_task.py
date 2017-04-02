from flask import Blueprint, request, jsonify, g
from flask_jwt import jwt_required
from schemas import task_schema
from models import Task

crud_task = Blueprint('crud_task', __name__)


@crud_task.route('', methods=["POST"])
@jwt_required()
def create():
    task, errors = task_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    task.save()

    return jsonify(task_schema.dump(task).data), 201


@crud_task.route('/<int:id>', methods=["GET"])
@jwt_required()
def read_one(id):
    try:
        task = Task.get(id=id)
        return jsonify(task_schema.dump(task).data)
    except Task.DoesNotExist:
        return jsonify({"message": "Can't find task with id - `{id}`".format(id=id)}), 404


@crud_task.route('/<int:id>', methods=["PUT"])
@jwt_required()
def update(id):
    try:
        task = Task.get(id=id)
    except Task.DoesNotExist:
        return jsonify({"message": "Can't find task with id - `{id}`".format(id=id)}), 404

    task, errors = task_schema.load(request.json, instance=task)

    if errors:
        return jsonify(errors), 400

    task.save()

    return jsonify(task_schema.dumps(task).data), 200


@crud_task.route('/<int:id>', methods=["DELETE"])
@jwt_required()
def delete(id):
    is_task_exists = Task.select().filter(id=id).exists()

    if not is_task_exists:
        return jsonify({"message": "Can't find task with id - `{id}`".format(id=id)}), 404

    Task.delete().where(Task.id == id).execute()
    return jsonify({}), 204
