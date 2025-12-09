from flask import request, jsonify
from app.events import events_bp
from app.events.services import EventService
from app.events.filters import EventFilters
from app.core.security import token_required


@events_bp.route('/active', methods=['GET'])
def get_active_events():
    events = EventFilters.get_active_events()
    return jsonify([e.to_dict() for e in events]), 200


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = EventService.get_event(event_id)
    return jsonify(event.to_dict() if event else {'error': 'Not found'}), (200 if event else 404)


@events_bp.route('/<int:event_id>/participate', methods=['POST'])
@token_required
def participate(event_id, current_user_id, current_role=None):
    result = EventService.participate(event_id, current_user_id)
    return jsonify(result), (200 if result['status'] == 'success' else 400)


@events_bp.route('/<int:event_id>/leave', methods=['POST'])
@token_required
def leave_event(event_id, current_user_id, current_role=None):
    result = EventService.leave_event(event_id, current_user_id)
    return jsonify(result), (200 if result['status'] == 'success' else 400)


@events_bp.route('/<int:event_id>/review', methods=['POST'])
@token_required
def add_review(event_id, current_user_id, current_role=None):
    data = request.get_json() or {}
    result = EventService.add_review(event_id, current_user_id, data.get('rating'), data.get('text'))
    return jsonify(result), (200 if result['status'] == 'success' else 400)
