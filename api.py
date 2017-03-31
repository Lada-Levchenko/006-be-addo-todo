from flask import Flask, request, jsonify, g
from flask_login import LoginManager, logout_user

from models import User, Project, Task, initialize
from schemas import user_schema, project_schema, task_schema
from blueprints.crud_user import crud_user
from blueprints.crud_project import crud_project
from blueprints.crud_task import crud_task
from flask_jwt import JWT, jwt_required, current_identity

from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'super secret key'
app.register_blueprint(crud_user, url_prefix="/api/user")
app.register_blueprint(crud_project, url_prefix="/api/project")
app.register_blueprint(crud_task, url_prefix="/api/task")
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['JWT_AUTH_URL_RULE'] = '/authenticate'
CORS(app=app)


def authenticate(username, password):
    user = User.filter(User.username == username).first()
    if user and user.password.check_password(password):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    try:
        return User.get(id=user_id)
    except User.DoesNotExist:
        return None

jwt = JWT(app, authenticate, identity)


@app.before_request
def before_request():
    g.user = current_identity


@app.route('/logout')
@jwt_required()
def logout():
    logout_user()
    return jsonify({}), 401


@app.route('/api/projects', methods=["GET"])
@jwt_required()
def get_projects_of_user():
    projects = list(Project.select().join(User).where(User.id == g.user.get_id()))
    return jsonify(project_schema.dump(projects, many=True)[0]), 200


@app.route('/api/tasks', methods=["GET"])
@jwt_required()
def get_tasks_of_project():
    id = request.args.get('project_id')
    if request.args.get('project_id'):
        project = Project.select().where(Project.id == id)
        if project.exists():
            if project.join(User).where(User.id == g.user.get_id()).exists():
                tasks = list(Task.select().join(Project).where(Project.id == id))
                return jsonify(task_schema.dump(tasks, many=True)[0]), 200
    return jsonify({}), 404

if __name__ == '__main__':
    initialize()
    app.run(use_reloader=True)
