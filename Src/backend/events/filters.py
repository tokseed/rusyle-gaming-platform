from app.events.models import Event, Participation
from datetime import datetime


class EventFilters:

    @staticmethod
    def get_active_events():
        return Event.query.filter(
            Event.status == 'active',
            Event.start_time > datetime.utcnow()
        ).all()

    @staticmethod
    def get_user_events(user_id):
        return Event.query.join(Participation).filter(
            Participation.user_id == user_id,
            Event.status == 'active'
        ).all()

    @staticmethod
    def get_past_events(user_id):
        return Event.query.join(Participation).filter(
            Participation.user_id == user_id,
            Event.status == 'past'
        ).all()
