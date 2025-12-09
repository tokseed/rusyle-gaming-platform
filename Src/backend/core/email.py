from flask import current_app
from flask_mail import Message
from app.extensions import mail


class EmailService:

    @staticmethod
    def send_verification_code(user, code):
        subject = 'Подтверждение регистрации'
        html = f"""
        <h2>Код подтверждения</h2>
        <p>Привет, {user.full_name}!</p>
        <h1 style="color: #2196F3; font-size: 32px; letter-spacing: 5px;">{code}</h1>
        <p>Код действителен 1 час.</p>
        """
        EmailService._send_email(user.email, subject, html)

    @staticmethod
    def send_welcome_email(user):
        subject = 'Добро пожаловать на RuSyle!'
        frontend_url = current_app.config['FRONTEND_URL']
        html = f"""
        <h2>Добро пожаловать!</h2>
        <p>Привет, {user.full_name}!</p>
        <p>Ваш аккаунт активирован.</p>
        <p><a href="{frontend_url}/auth/login">Войти</a></p>
        """
        EmailService._send_email(user.email, subject, html)

    @staticmethod
    def send_password_reset_link(user, token):
        frontend_url = current_app.config['FRONTEND_URL']
        reset_link = f"{frontend_url}/auth/reset-password/{token}"
        subject = 'Восстановление пароля'
        html = f"""
        <h2>Восстановление пароля</h2>
        <p>Привет, {user.full_name}!</p>
        <p><a href="{reset_link}">Сбросить пароль</a></p>
        <p>Ссылка действительна 24 часа.</p>
        """
        EmailService._send_email(user.email, subject, html)

    @staticmethod
    def send_password_changed_notification(user):
        subject = 'Пароль изменен'
        html = f"""
        <h2>Пароль изменен</h2>
        <p>Привет, {user.full_name}!</p>
        <p>Ваш пароль успешно изменен.</p>
        """
        EmailService._send_email(user.email, subject, html)

    @staticmethod
    def send_event_reminder(user, event):
        frontend_url = current_app.config['FRONTEND_URL']
        subject = f'Напоминание: {event.title} завтра!'
        html = f"""
        <h2>Напоминание о событии</h2>
        <p>Привет, {user.full_name}!</p>
        <p>Событие <strong>{event.title}</strong> начинается завтра.</p>
        <p><a href="{frontend_url}/events/{event.id}">Перейти</a></p>
        """
        EmailService._send_email(user.email, subject, html)

    @staticmethod
    def _send_email(to, subject, html):
        try:
            msg = Message(subject=subject, recipients=[to], html=html)
            mail.send(msg)
        except Exception as e:
            print(f"Email error: {str(e)}")
