from flask import request, jsonify
from app.admin import admin_bp
from app.admin.services import AdminService
from app.admin.decorators import admin_only
from app.core.security import token_required


@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_only
def get_users(current_user_id, current_role=None):
    page = request.args.get('page', 1, type=int)
    users = AdminService.get_users(page=page)
    return jsonify({'users': [u.to_dict() for u in users.items], 'total': users.total}), 200


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_only
def update_user(user_id, current_user_id, current_role=None):
    result = AdminService.update_user(user_id, request.get_json() or {})
    return jsonify(result), (200 if result['status'] == 'success' else 400)


@admin_bp.route('/events', methods=['POST'])
@token_required
@admin_only
def create_event(current_user_id, current_role=None):
    result = AdminService.create_event(request.get_json() or {})
    return jsonify(result), (201 if result['status'] == 'success' else 400)


@admin_bp.route('/events/<int:event_id>/export', methods=['GET'])
@token_required
@admin_only
def export_participants(event_id, current_user_id, current_role=None):
    result = AdminService.export_participants(event_id)
    return jsonify(result), (200 if result['status'] == 'success' else 400)
