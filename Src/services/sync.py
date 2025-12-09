"""
services/sync.py

Сервис для экспорта данных в CSV и работы с кешем.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Optional, Literal
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
        def error(msg):
            print(f"[ERROR] {msg}")


    logger = SimpleLogger()


def export_to_csv(
        export_type: Literal["users", "games", "events"],
        output_path: Optional[str] = None,
) -> str:
    """
    Экспорт данных в CSV.
    export_type: 'users' | 'games' | 'events'
    Возвращает путь к созданному файлу.
    """
    base_path = Path("data")
    base_path.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        output_path = base_path / f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    else:
        output_path = Path(output_path)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        if export_type == "users":
            # Загрузить пользователей
            users_file = Path("data/users.json")
            if users_file.exists():
                with open(users_file, "r", encoding="utf-8") as uf:
                    users_data = json.load(uf)
                writer.writerow(["ID", "Логин", "Роль"])
                for u in users_data.get("users", []):
                    writer.writerow([u["id"], u["username"], u["role"]])

        elif export_type == "games":
            # Загрузить игры
            games_file = Path("data/games.json")
            if games_file.exists():
                with open(games_file, "r", encoding="utf-8") as gf:
                    games_data = json.load(gf)
                writer.writerow(["ID", "Название", "Жанр", "Разработчик", "Дата выхода", "Активна"])
                for g in games_data.get("games", []):
                    writer.writerow([
                        g["id"],
                        g["title"],
                        g["genre"],
                        g["developer_name"],
                        g.get("release_date", ""),
                        "Да" if g["is_active"] else "Нет",
                    ])

        elif export_type == "events":
            # Загрузить события
            events_file = Path("data/events.json")
            if events_file.exists():
                with open(events_file, "r", encoding="utf-8") as ef:
                    events_data = json.load(ef)
                writer.writerow(["ID", "Название", "Тип", "Город", "Начало", "Конец", "Игра", "Активно"])
                for e in events_data.get("events", []):
                    writer.writerow([
                        e["id"],
                        e["title"],
                        e["event_type"],
                        e["city"],
                        e["start_at"],
                        e.get("end_at", ""),
                        e.get("game_id", ""),
                        "Да" if e["is_active"] else "Нет",
                    ])

    logger.info(f"[sync] Данные '{export_type}' экспортированы в {output_path}")
    return str(output_path)


# ===== Кеш =====

CACHE_FILE = Path("data/cache.json")


def load_cache() -> dict:
    """Загрузка кеша из файла"""
    if not CACHE_FILE.exists():
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"[sync] Ошибка чтения cache.json: {e}")
        return {}


def save_cache(data: dict) -> None:
    """Сохранение кеша в файл"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"[sync] Кеш сохранён в {CACHE_FILE}")
    except Exception as e:
        logger.error(f"[sync] Ошибка записи cache.json: {e}")


def get_cache(key: str, default=None):
    """Получить значение из кеша"""
    cache = load_cache()
    return cache.get(key, default)


def set_cache(key: str, value) -> None:
    """Установить значение в кеш"""
    cache = load_cache()
    cache[key] = value
    save_cache(cache)
