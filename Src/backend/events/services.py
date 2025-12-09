from datetime import datetime, timedelta
from app.events.models import Event, Participation, Review
from app.extensions import db


class EventService:

    @staticmethod
    def get_event(event_id):
        return Event.query.get(event_id)

    @staticmethod
    def participate(event_id, user_id):
        try:
            event = Event.query.get(event_id)
            if not event:
                return {'status': 'error', 'message': 'Event not found'}

            if len(event.participations) >= event.max_participants:
                return {'status': 'error', 'message': 'Event full'}

            if Participation.query.filter_by(event_id=event_id, user_id=user_id).first():
                return {'status': 'error', 'message': 'Already participating'}

            p = Participation(event_id=event_id, user_id=user_id)
            db.session.add(p)
            db.session.commit()

            return {'status': 'success', 'message': 'Confirmed'}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def leave_event(event_id, user_id):
        try:
            p = Participation.query.filter_by(event_id=event_id, user_id=user_id).first()
            if not p:
                return {'status': 'error', 'message': 'Not participating'}

            db.session.delete(p)
            db.session.commit()

            return {'status': 'success', 'message': 'Left'}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def add_review(event_id, user_id, rating, text):
        try:
            review = Review(event_id=event_id, user_id=user_id, rating=rating, text=text)
            db.session.add(review)
            db.session.commit()

            return {'status': 'success', 'message': 'Review added'}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}
