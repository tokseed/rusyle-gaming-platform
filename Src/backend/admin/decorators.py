from functools import wraps
from flask import jsonify


def admin_only(f):
    @wraps(f)
    def decorated(*args, current_role=None, **kwargs):
        if current_role != 'admin':
            return jsonify({'error': 'Admin required'}), 403
        return f(*args, current_role=current_role, **kwargs)
    return decorated
