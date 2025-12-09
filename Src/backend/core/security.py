from flask import request, jsonify, current_app
from functools import wraps
import jwt
from datetime import datetime, timedelta


def create_access_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=168),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'],
                      algorithm=current_app.config['JWT_ALGORITHM'])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token missing'}), 401

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'],
                                 algorithms=[current_app.config['JWT_ALGORITHM']])
            current_user_id = payload['user_id']
            current_role = payload['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user_id, current_role=current_role, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, current_role=None, **kwargs):
        if current_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)

    return decorated
