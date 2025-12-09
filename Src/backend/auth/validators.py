import re
from app.auth.models import User


class ValidationError(Exception):
    pass


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Некорректный email')
    return True


def validate_email_unique(email):
    if User.query.filter_by(email=email).first():
        raise ValidationError('Email зарегистрирован')
    return True


def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Минимум 8 символов')

    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    if not (has_upper and has_lower and has_digit and has_special):
        raise ValidationError('Буквы, цифры, спецсимволы обязательны')
    return True


def validate_passwords_match(password, password_confirm):
    if password != password_confirm:
        raise ValidationError('Пароли не совпадают')
    return True


def validate_full_name(full_name):
    pattern = r'^[А-Яа-яЁё\s]+$'
    if not full_name.strip() or not re.match(pattern, full_name):
        raise ValidationError('Только русские буквы и пробелы')
    return True


def validate_verification_code(code):
    if not re.match(r'^\d{6}$', code):
        raise ValidationError('6 цифр')
    return True
