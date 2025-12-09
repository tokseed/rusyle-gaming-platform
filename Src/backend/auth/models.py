from app.extensions import db
from datetime import datetime, timedelta
import secrets
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    status = db.Column(db.String(20), default='inactive')
    email_verified_at = db.Column(db.DateTime)
    theme = db.Column(db.String(10), default='light')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    participations = db.relationship('Participation', backref='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'theme': self.theme,
            'created_at': self.created_at.isoformat()
        }


class EmailVerification(db.Model):
    __tablename__ = 'email_verifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    verified_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('verifications', cascade='all, delete-orphan'))

    @staticmethod
    def generate_code():
        return str(secrets.randbelow(999999)).zfill(6)

    def is_valid(self):
        return not self.verified_at and self.expires_at > datetime.utcnow()


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('password_resets', cascade='all, delete-orphan'))

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    def is_valid(self):
        return not self.used_at and self.expires_at > datetime.utcnow()
