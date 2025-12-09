"""
services/games.py

Сервис для работы с играми.
Хранит игры в JSON-файле.
"""

import json
import sys
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.logger import logger
except ImportError:
    class SimpleLogger:
        @staticmethod
        def info(msg):
            print(f"[INFO] {msg}")

        @staticmethod
        def warning(msg):
            print(f"[WARN] {msg}")


    logger = SimpleLogger()

from services.auth import AuthUser, is_admin, is_developer

GAMES_FILE = Path("data/games.json")


@dataclass
class GameDTO:
    id: int
    title: str
    description: str
    genre: str
    developer_name: str
    release_date: Optional[str]
    is_active: bool


def _ensure_games_file():
    """Создать файл игр, если его нет"""
    GAMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not GAMES_FILE.exists():
        GAMES_FILE.write_text(json.dumps({"games": [], "next_id": 1}, ensure_ascii=False, indent=2))


def _load_games() -> dict:
    """Загрузить игры из файла"""
    _ensure_games_file()
    with open(GAMES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_games(data: dict) -> None:
    """Сохранить игры в файл"""
    _ensure_games_file()
    with open(GAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def list_games(
        genre: Optional[str] = None,
        active_only: bool = True,
) -> List[GameDTO]:
    """Получение списка игр с опциональной фильтрацией"""
    data = _load_games()
    games = data["games"]

    if genre:
        games = [g for g in games if g["genre"].lower() == genre.lower()]
    if active_only:
        games = [g for g in games if g["is_active"]]

    games = sorted(games, key=lambda x: x["title"])
    return [GameDTO(**g) for g in games]


def get_game(game_id: int) -> Optional[GameDTO]:
    """Получение информации об одной игре"""
    data = _load_games()
    for game in data["games"]:
        if game["id"] == game_id:
            return GameDTO(**game)
    return None


def create_game(
        current_user: AuthUser,
        title: str,
        description: str,
        genre: str,
        developer_name: Optional[str] = None,
        release_date: Optional[str] = None,
) -> GameDTO:
    """Создание новой игры (разработчик или админ)"""
    if not (is_admin(current_user) or is_developer(current_user)):
        raise PermissionError("Недостаточно прав для создания игры")

    data = _load_games()
    dev_name = developer_name or current_user.username

    game_id = data["next_id"]
    new_game = {
        "id": game_id,
        "title": title,
        "description": description,
        "genre": genre,
        "developer_name": dev_name,
        "release_date": release_date,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
    }

    data["games"].append(new_game)
    data["next_id"] = game_id + 1
    _save_games(data)

    logger.info(f"[games] Создана игра '{title}' разработчиком {dev_name}")
    return GameDTO(**new_game)


def update_game(
        current_user: AuthUser,
        game_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        genre: Optional[str] = None,
        is_active: Optional[bool] = None,
) -> GameDTO:
    """Обновление информации об игре"""
    data = _load_games()

    game = None
    game_idx = None
    for idx, g in enumerate(data["games"]):
        if g["id"] == game_id:
            game = g
            game_idx = idx
            break

    if not game:
        raise ValueError("Игра не найдена")

    # Проверка прав
    if not is_admin(current_user) and game["developer_name"] != current_user.username:
        raise PermissionError("Недостаточно прав для редактирования этой игры")

    if title is not None:
        game["title"] = title
    if description is not None:
        game["description"] = description
    if genre is not None:
        game["genre"] = genre
    if is_active is not None:
        game["is_active"] = is_active

    data["games"][game_idx] = game
    _save_games(data)

    logger.info(f"[games] Обновлена игра id={game_id} пользователем {current_user.username}")
    return GameDTO(**game)


def delete_game(current_user: AuthUser, game_id: int) -> None:
    """Удаление игры"""
    data = _load_games()

    game = None
    game_idx = None
    for idx, g in enumerate(data["games"]):
        if g["id"] == game_id:
            game = g
            game_idx = idx
            break

    if not game:
        raise ValueError("Игра не найдена")

    if not is_admin(current_user) and game["developer_name"] != current_user.username:
        raise PermissionError("Недостаточно прав для удаления этой игры")

    data["games"].pop(game_idx)
    _save_games(data)

    logger.info(f"[games] Удалена игра id={game_id} пользователем {current_user.username}")


def subscribe_to_game(current_user: AuthUser, game_id: int) -> None:
    """Подписка пользователя на игру"""
    data = _load_games()

    game = None
    for g in data["games"]:
        if g["id"] == game_id:
            game = g
            break

    if not game:
        raise ValueError("Игра не найдена")

    # Загружаем подписки
    subs_data = _load_subscriptions()
    sub_key = f"{current_user.id}_{game_id}"

    if sub_key in subs_data["subscriptions"]:
        logger.info(f"[games] Пользователь {current_user.username} уже подписан на игру id={game_id}")
        return

    subs_data["subscriptions"][sub_key] = {
        "user_id": current_user.id,
        "game_id": game_id,
        "subscribed_at": datetime.now().isoformat(),
    }
    _save_subscriptions(subs_data)

    logger.info(f"[games] Пользователь {current_user.username} подписался на игру id={game_id}")


def unsubscribe_from_game(current_user: AuthUser, game_id: int) -> None:
    """Отписка пользователя от игры"""
    subs_data = _load_subscriptions()
    sub_key = f"{current_user.id}_{game_id}"

    if sub_key in subs_data["subscriptions"]:
        del subs_data["subscriptions"][sub_key]
        _save_subscriptions(subs_data)

    logger.info(f"[games] Пользователь id={current_user.id} отписался от игры id={game_id}")


def list_user_subscriptions(current_user: AuthUser) -> List[GameDTO]:
    """Получить список игр, на которые подписан пользователь"""
    subs_data = _load_subscriptions()
    games_data = _load_games()

    game_ids = [
        int(sub["game_id"])
        for sub in subs_data["subscriptions"].values()
        if sub["user_id"] == current_user.id
    ]

    result = []
    for game in games_data["games"]:
        if game["id"] in game_ids:
            result.append(GameDTO(**game))

    return result


# ===== Вспомогательные функции для подписок =====

SUBSCRIPTIONS_FILE = Path("data/subscriptions.json")


def _ensure_subscriptions_file():
    """Создать файл подписок, если его нет"""
    SUBSCRIPTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not SUBSCRIPTIONS_FILE.exists():
        SUBSCRIPTIONS_FILE.write_text(json.dumps({"subscriptions": {}}, ensure_ascii=False, indent=2))


def _load_subscriptions() -> dict:
    """Загрузить подписки из файла"""
    _ensure_subscriptions_file()
    with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_subscriptions(data: dict) -> None:
    """Сохранить подписки в файл"""
    _ensure_subscriptions_file()
    with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
