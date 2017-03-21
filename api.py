from flask import Flask, request, jsonify
from models import User, Project, Task, initialize
from schemas import user_schema, project_schema, task_schema
from blueprints.crud_user import crud_user
from blueprints.crud_project import crud_project
from blueprints.crud_task import crud_task

from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(crud_user, url_prefix="/api/users")
app.register_blueprint(crud_project, url_prefix="/api/projects")
app.register_blueprint(crud_task, url_prefix="/api/tasks")
CORS(app=app)
initialize()


@app.route('/api/users/<int:id>/projects', methods=["GET"])
def get_projects_of_user(id):
    projects = list(Project.select().join(User).where(User.id == id))
    return jsonify(project_schema.dump(projects, many=True)), 200


@app.route('/api/projects/<int:id>/tasks', methods=["GET"])
def get_tasks_of_project(id):
    tasks = list(Task.select().join(Project).where(Project.id == id))
    return jsonify(task_schema.dump(tasks, many=True)), 200

if __name__ == '__main__':
    initialize()
    app.run(use_reloader=True)
