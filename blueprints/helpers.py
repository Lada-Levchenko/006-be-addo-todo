from flask import jsonify, g
from functools import wraps


def user_check_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.get_id() != kwargs["id"]:
            return jsonify({}), 403
        return f(*args, **kwargs)
    return decorated_function