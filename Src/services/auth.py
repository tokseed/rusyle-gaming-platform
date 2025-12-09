"""
services/auth.py

Сервис авторизации и управления пользователями.
Хранит пользователей в JSON-файле.
"""

import json
import sys
from typing import Optional, List
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from datetime import datetime

# Добавляем parent directory в sys.path для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.logger import logger
except ImportError:
    # Fallback логирование, если logger не доступен
    class SimpleLogger:
        @staticmethod
        def info(msg):
            print(f"[INFO] {msg}")

        @staticmethod
        def warning(msg):
            print(f"[WARN] {msg}")


    logger = SimpleLogger()

ROLE_USER = "user"
ROLE_DEVELOPER = "developer"
ROLE_ADMIN = "admin"

VALID_ROLES = {ROLE_USER, ROLE_DEVELOPER, ROLE_ADMIN}

# Путь к файлу с пользователями
USERS_FILE = Path("data/users.json")


@dataclass
class AuthUser:
    """Объект авторизованного пользователя"""
    id: int
    username: str
    role: str


def _ensure_users_file():
    """Создать файл пользователей, если его нет"""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps({"users": [], "next_id": 1}, ensure_ascii=False, indent=2))


def _load_users() -> dict:
    """Загрузить пользователей из файла"""
    _ensure_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_users(data: dict) -> None:
    """Сохранить пользователей в файл"""
    _ensure_users_file()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def hash_password(password: str) -> str:
    """Хэширование пароля"""
    return sha256(password.encode("utf-8")).hexdigest()


def register_user(username: str, password: str, role: str = ROLE_USER) -> AuthUser:
    """Регистрация нового пользователя"""
    if role not in VALID_ROLES:
        raise ValueError(f"Недопустимая роль: {role}")

    data = _load_users()

    # Проверка, что пользователя с таким логином нет
    if any(u["username"] == username for u in data["users"]):
        raise ValueError("Пользователь с таким логином уже существует")

    user_id = data["next_id"]
    new_user = {
        "id": user_id,
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "created_at": datetime.now().isoformat(),
    }

    data["users"].append(new_user)
    data["next_id"] = user_id + 1

    _save_users(data)
    logger.info(f"[auth] Зарегистрирован пользователь: {username} (role={role})")

    return AuthUser(id=user_id, username=username, role=role)


def authenticate(username: str, password: str) -> Optional[AuthUser]:
    """Аутентификация пользователя"""
    data = _load_users()
    password_h = hash_password(password)

    for user in data["users"]:
        if user["username"] == username and user["password_hash"] == password_h:
            logger.info(f"[auth] Успешный вход: {username}")
            return AuthUser(id=user["id"], username=user["username"], role=user["role"])

    logger.warning(f"[auth] Неуспешная попытка входа: {username}")
    return None


def get_user_by_id(user_id: int) -> Optional[AuthUser]:
    """Получение пользователя по ID"""
    data = _load_users()
    for user in data["users"]:
        if user["id"] == user_id:
            return AuthUser(id=user["id"], username=user["username"], role=user["role"])
    return None


def get_user_by_username(username: str) -> Optional[AuthUser]:
    """Получение пользователя по имени"""
    data = _load_users()
    for user in data["users"]:
        if user["username"] == username:
            return AuthUser(id=user["id"], username=user["username"], role=user["role"])
    return None


def is_admin(user: AuthUser) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user.role == ROLE_ADMIN


def is_developer(user: AuthUser) -> bool:
    """Проверка, является ли пользователь разработчиком"""
    return user.role == ROLE_DEVELOPER


def has_any_role(user: AuthUser, roles: List[str]) -> bool:
    """Проверка, есть ли у пользователя одна из указанных ролей"""
    return user.role in roles


def list_all_users() -> List[AuthUser]:
    """Список всех пользователей (для админ-панели)"""
    data = _load_users()
    return [
        AuthUser(id=u["id"], username=u["username"], role=u["role"])
        for u in data["users"]
    ]
