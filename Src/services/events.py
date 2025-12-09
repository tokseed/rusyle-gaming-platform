"""
services/events.py

Сервис для работы с событиями.
Хранит события в JSON-файле.
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

EVENTS_FILE = Path("data/events.json")
COMMENTS_FILE = Path("data/comments.json")


@dataclass
class EventDTO:
    id: int
    title: str
    description: str
    event_type: str
    city: str
    start_at: str
    end_at: Optional[str]
    game_id: Optional[int]
    game_title: Optional[str]
    is_active: bool


@dataclass
class CommentDTO:
    id: int
    user_name: str
    text: str
    rating: Optional[int]
    created_at: str


def _ensure_events_file():
    """Создать файл событий, если его нет"""
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not EVENTS_FILE.exists():
        EVENTS_FILE.write_text(json.dumps({"events": [], "next_id": 1}, ensure_ascii=False, indent=2))


def _ensure_comments_file():
    """Создать файл комментариев, если его нет"""
    COMMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not COMMENTS_FILE.exists():
        COMMENTS_FILE.write_text(json.dumps({"comments": [], "next_id": 1}, ensure_ascii=False, indent=2))


def _load_events() -> dict:
    """Загрузить события из файла"""
    _ensure_events_file()
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_events(data: dict) -> None:
    """Сохранить события в файл"""
    _ensure_events_file()
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_comments() -> dict:
    """Загрузить комментарии из файла"""
    _ensure_comments_file()
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_comments(data: dict) -> None:
    """Сохранить комментарии в файл"""
    _ensure_comments_file()
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_game_title(game_id: Optional[int]) -> Optional[str]:
    """Получить название игры по ID (из games.json)"""
    if not game_id:
        return None
    try:
        from services.games import get_game
        game = get_game(game_id)
        return game.title if game else None
    except Exception:
        return None


def list_events(
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        city: Optional[str] = None,
        event_type: Optional[str] = None,
        game_id: Optional[int] = None,
        upcoming_only: bool = True,
) -> List[EventDTO]:
    """Получение списка событий с фильтрами"""
    data = _load_events()
    events = data["events"]

    if city:
        events = [e for e in events if e["city"].lower() == city.lower()]
    if event_type:
        events = [e for e in events if e["event_type"].lower() == event_type.lower()]
    if game_id:
        events = [e for e in events if e["game_id"] == game_id]
    if upcoming_only:
        now = datetime.now().isoformat()
        events = [e for e in events if e["start_at"] >= now]

    events = sorted(events, key=lambda x: x["start_at"])

    result = []
    for e in events:
        result.append(EventDTO(
            id=e["id"],
            title=e["title"],
            description=e["description"],
            event_type=e["event_type"],
            city=e["city"],
            start_at=e["start_at"],
            end_at=e.get("end_at"),
            game_id=e.get("game_id"),
            game_title=_get_game_title(e.get("game_id")),
            is_active=e["is_active"],
        ))

    return result


def get_event(event_id: int) -> Optional[EventDTO]:
    """Получение информации об одном событии"""
    data = _load_events()
    for e in data["events"]:
        if e["id"] == event_id:
            return EventDTO(
                id=e["id"],
                title=e["title"],
                description=e["description"],
                event_type=e["event_type"],
                city=e["city"],
                start_at=e["start_at"],
                end_at=e.get("end_at"),
                game_id=e.get("game_id"),
                game_title=_get_game_title(e.get("game_id")),
                is_active=e["is_active"],
            )
    return None


def create_event(
        current_user: AuthUser,
        title: str,
        description: str,
        event_type: str,
        city: str,
        start_at: str,
        end_at: Optional[str] = None,
        game_id: Optional[int] = None,
) -> EventDTO:
    """Создание события (разработчик или админ)"""
    if not (is_admin(current_user) or is_developer(current_user)):
        raise PermissionError("Недостаточно прав для создания события")

    data = _load_events()

    event_id = data["next_id"]
    new_event = {
        "id": event_id,
        "title": title,
        "description": description,
        "event_type": event_type,
        "city": city,
        "start_at": start_at,
        "end_at": end_at,
        "game_id": game_id,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "created_by": current_user.username,
    }

    data["events"].append(new_event)
    data["next_id"] = event_id + 1
    _save_events(data)

    logger.info(f"[events] Создано событие '{title}' ({event_type}) в городе {city}")

    return EventDTO(
        id=event_id,
        title=title,
        description=description,
        event_type=event_type,
        city=city,
        start_at=start_at,
        end_at=end_at,
        game_id=game_id,
        game_title=_get_game_title(game_id),
        is_active=True,
    )


def update_event(
        current_user: AuthUser,
        event_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        event_type: Optional[str] = None,
        city: Optional[str] = None,
        start_at: Optional[str] = None,
        end_at: Optional[str] = None,
        is_active: Optional[bool] = None,
) -> EventDTO:
    """Обновление события (только админ)"""
    if not is_admin(current_user):
        raise PermissionError("Редактировать события может только администратор")

    data = _load_events()

    event = None
    event_idx = None
    for idx, e in enumerate(data["events"]):
        if e["id"] == event_id:
            event = e
            event_idx = idx
            break

    if not event:
        raise ValueError("Событие не найдено")

    if title is not None:
        event["title"] = title
    if description is not None:
        event["description"] = description
    if event_type is not None:
        event["event_type"] = event_type
    if city is not None:
        event["city"] = city
    if start_at is not None:
        event["start_at"] = start_at
    if end_at is not None:
        event["end_at"] = end_at
    if is_active is not None:
        event["is_active"] = is_active

    data["events"][event_idx] = event
    _save_events(data)

    logger.info(f"[events] Обновлено событие id={event_id} админом {current_user.username}")

    return EventDTO(
        id=event["id"],
        title=event["title"],
        description=event["description"],
        event_type=event["event_type"],
        city=event["city"],
        start_at=event["start_at"],
        end_at=event.get("end_at"),
        game_id=event.get("game_id"),
        game_title=_get_game_title(event.get("game_id")),
        is_active=event["is_active"],
    )


def delete_event(current_user: AuthUser, event_id: int) -> None:
    """Удаление события (только админ)"""
    if not is_admin(current_user):
        raise PermissionError("Удалять события может только администратор")

    data = _load_events()

    event_idx = None
    for idx, e in enumerate(data["events"]):
        if e["id"] == event_id:
            event_idx = idx
            break

    if event_idx is None:
        raise ValueError("Событие не найдено")

    data["events"].pop(event_idx)
    _save_events(data)

    logger.info(f"[events] Удалено событие id={event_id} админом {current_user.username}")


def add_comment(
        current_user: AuthUser,
        event_id: int,
        text: str,
        rating: Optional[int] = None,
) -> CommentDTO:
    """Добавление комментария к событию"""
    data = _load_comments()

    comment_id = data["next_id"]
    new_comment = {
        "id": comment_id,
        "event_id": event_id,
        "user_id": current_user.id,
        "user_name": current_user.username,
        "text": text,
        "rating": rating,
        "created_at": datetime.now().isoformat(),
    }

    data["comments"].append(new_comment)
    data["next_id"] = comment_id + 1
    _save_comments(data)

    logger.info(f"[events] Пользователь {current_user.username} оставил комментарий к событию id={event_id}")

    return CommentDTO(
        id=comment_id,
        user_name=current_user.username,
        text=text,
        rating=rating,
        created_at=new_comment["created_at"],
    )


def list_event_comments(event_id: int) -> List[CommentDTO]:
    """Список комментариев к событию"""
    data = _load_comments()

    comments = [c for c in data["comments"] if c["event_id"] == event_id]
    comments = sorted(comments, key=lambda x: x["created_at"], reverse=True)

    return [
        CommentDTO(
            id=c["id"],
            user_name=c["user_name"],
            text=c["text"],
            rating=c.get("rating"),
            created_at=c["created_at"],
        )
        for c in comments
    ]
