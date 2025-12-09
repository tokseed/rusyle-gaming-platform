from datetime import datetime, timedelta
from app.auth.models import User, EmailVerification, PasswordReset
from app.auth.validators import *
from app.extensions import db
from app.core.email import EmailService
from app.core.security import create_access_token


class AuthService:

    @staticmethod
    def register(data):
        try:
            validate_full_name(data.get('full_name', ''))
            validate_email(data.get('email', ''))
            validate_email_unique(data.get('email', ''))
            validate_password(data.get('password', ''))
            validate_passwords_match(data.get('password', ''), data.get('password_confirm', ''))

            user = User(full_name=data['full_name'], email=data['email'],
                        role='user', status='inactive')
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()

            code = EmailVerification.generate_code()
            email_ver = EmailVerification(user_id=user.id, code=code,
                                          expires_at=datetime.utcnow() + timedelta(hours=1))
            db.session.add(email_ver)
            db.session.commit()

            EmailService.send_verification_code(user, code)

            return {'status': 'success', 'message': 'Письмо отправлено', 'user_id': user.id}
        except ValidationError as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def verify_email(user_id, code):
        try:
            validate_verification_code(code)
            email_ver = EmailVerification.query.filter_by(user_id=user_id, code=code).first()

            if not email_ver or not email_ver.is_valid():
                return {'status': 'error', 'message': 'Неверный код'}

            user = User.query.get(user_id)
            user.status = 'active'
            user.email_verified_at = datetime.utcnow()
            email_ver.verified_at = datetime.utcnow()
            db.session.commit()

            EmailService.send_welcome_email(user)

            return {'status': 'success', 'message': 'Email подтвержден'}
        except ValidationError as e:
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def login(email, password):
        try:
            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                return {'status': 'error', 'message': 'Неверные данные'}

            if user.status == 'deleted':
                return {'status': 'error', 'message': 'Аккаунт удален'}

            if user.status == 'inactive':
                return {'status': 'error', 'message': 'Email не подтвержден'}

            token = create_access_token(user.id, user.role)
            return {'status': 'success', 'token': token, 'user': user.to_dict()}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def forgot_password(email):
        try:
            user = User.query.filter_by(email=email).first()

            if not user:
                return {'status': 'success', 'message': 'Письмо отправлено'}

            PasswordReset.query.filter_by(user_id=user.id, used_at=None).delete()

            token = PasswordReset.generate_token()
            reset = PasswordReset(user_id=user.id, token=token,
                                  expires_at=datetime.utcnow() + timedelta(hours=24))
            db.session.add(reset)
            db.session.commit()

            EmailService.send_password_reset_link(user, token)

            return {'status': 'success', 'message': 'Письмо отправлено'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def reset_password(token, password, password_confirm):
        try:
            validate_password(password)
            validate_passwords_match(password, password_confirm)

            reset = PasswordReset.query.filter_by(token=token).first()

            if not reset or not reset.is_valid():
                return {'status': 'error', 'message': 'Ссылка истекла'}

            user = User.query.get(reset.user_id)
            user.set_password(password)
            reset.used_at = datetime.utcnow()
            db.session.commit()

            EmailService.send_password_changed_notification(user)

            return {'status': 'success', 'message': 'Пароль изменен'}
        except ValidationError as e:
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}
