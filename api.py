from flask import Flask, request, jsonify, g
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from models import User, Project, Task, initialize
from schemas import user_schema, project_schema, task_schema
from blueprints.crud_user import crud_user
from blueprints.crud_project import crud_project
from blueprints.crud_task import crud_task

from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'super secret key'
app.register_blueprint(crud_user, url_prefix="/api/user")
app.register_blueprint(crud_project, url_prefix="/api/project")
app.register_blueprint(crud_task, url_prefix="/api/task")
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app=app)


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    registered_user = User.filter(User.username == username).first()

    if registered_user is None:
        return jsonify({}), 404

    if not registered_user.password.check_password(password):
        return jsonify({}), 401

    login_user(registered_user)
    app.register_blueprint(crud_user, url_prefix="/api/users")
    app.register_blueprint(crud_project, url_prefix="/api/projects")
    app.register_blueprint(crud_task, url_prefix="/api/tasks")
    return jsonify({}), 202


@app.route('/logout')
def logout():
    logout_user()
    app.blueprints.clear()
    return jsonify({}), 401


@app.route('/api/projects', methods=["GET"])
@login_required
def get_projects_of_user():
    projects = list(Project.select().join(User).where(User.id == g.user.get_id()))
    return jsonify(project_schema.dump(projects, many=True)), 200


@app.route('/api/tasks', methods=["GET"])
@login_required
def get_tasks_of_project():
    id = request.args.get('project_id')
    if request.args.get('project_id'):
        project = Project.select().where(Project.id == id)
        if project.exists():
            if project.join(User).where(User.id == g.user.get_id()).exists():
                tasks = list(Task.select().join(Project).where(Project.id == id))
                return jsonify(task_schema.dump(tasks, many=True)), 200
    return jsonify({}), 404

if __name__ == '__main__':
    initialize()
    app.run(use_reloader=True)
