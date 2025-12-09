from app.auth.models import User
from app.events.models import Event, Participation
from app.extensions import db
import csv
from io import StringIO


class AdminService:

    @staticmethod
    def get_users(page=1, limit=20):
        return User.query.paginate(page=page, per_page=limit)

    @staticmethod
    def update_user(user_id, data):
        try:
            user = User.query.get(user_id)
            if not user:
                return {'status': 'error', 'message': 'Not found'}

            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'role' in data:
                user.role = data['role']
            if 'status' in data:
                user.status = data['status']

            db.session.commit()
            return {'status': 'success', 'message': 'Updated'}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def create_event(data):
        try:
            event = Event(
                title=data['title'],
                description=data.get('description'),
                start_time=data['start_time'],
                end_time=data['end_time'],
                location=data.get('location'),
                image_url=data.get('image_url'),
                max_participants=data.get('max_participants'),
                payment_required=data.get('payment_required', False),
                price=data.get('price')
            )
            db.session.add(event)
            db.session.commit()

            return {'status': 'success', 'message': 'Created', 'event_id': event.id}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def export_participants(event_id):
        try:
            participants = Participation.query.filter_by(event_id=event_id).all()

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'Full Name', 'Email', 'Date'])

            for p in participants:
                writer.writerow([p.user.id, p.user.full_name, p.user.email, p.created_at])

            return {'status': 'success', 'data': output.getvalue()}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
