from flask import Blueprint, request, jsonify, g
from flask_jwt import jwt_required
from schemas import project_schema
from models import Project

crud_project = Blueprint('crud_project', __name__)


@crud_project.route('', methods=["POST"])
@jwt_required()
def create():
    project, errors = project_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    project.user = g.user.get_id()
    project.save()

    return jsonify(project_schema.dump(project).data), 201


@crud_project.route('', methods=["GET"])
def read():
    projects = list(Project.select())
    return jsonify(project_schema.dump(projects, many=True).data)


@crud_project.route('/<int:id>', methods=["GET"])
def read_one(id):
    try:
        project = Project.get(id=id)
        return jsonify(project_schema.dump(project).data)
    except Project.DoesNotExist:
        return jsonify({"message": "Can't find project with id - `{id}`".format(id=id)}), 404


@crud_project.route('/<int:id>', methods=["PUT"])
def update(id):
    try:
        project = Project.get(id=id)
    except Project.DoesNotExist:
        return jsonify({"message": "Can't find project with id - `{id}`".format(id=id)}), 404

    project, errors = project_schema.load(request.json, instance=project)

    if errors:
        return jsonify(errors), 400

    project.save()

    return jsonify(project_schema.dumps(project).data), 200


@crud_project.route('/<int:id>', methods=["DELETE"])
def delete(id):
    is_project_exists = Project.select().filter(id=id).exists()

    if not is_project_exists:
        return jsonify({"message": "Can't find project with id - `{id}`".format(id=id)}), 404

    Project.delete().where(Project.id == id).execute()
    return jsonify({}), 204
