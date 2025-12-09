from flask import request, jsonify
from app.auth import auth_bp
from app.auth.services import AuthService
from app.core.security import token_required


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result = AuthService.register(data or {})
    return jsonify(result), (201 if result['status'] == 'success' else 400)


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json() or {}
    result = AuthService.verify_email(data.get('user_id'), data.get('code'))
    return jsonify(result), (200 if result['status'] == 'success' else 400)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    result = AuthService.login(data.get('email'), data.get('password'))
    return jsonify(result), (200 if result['status'] == 'success' else 401)


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    result = AuthService.forgot_password(data.get('email'))
    return jsonify(result), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json() or {}
    result = AuthService.reset_password(token, data.get('password'), data.get('password_confirm'))
    return jsonify(result), (200 if result['status'] == 'success' else 400)


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user_id, current_role=None):
    from app.auth.models import User
    user = User.query.get(current_user_id)
    return jsonify(user.to_dict() if user else {'error': 'Not found'}), (200 if user else 404)
