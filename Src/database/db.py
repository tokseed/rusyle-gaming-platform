"""
Модуль для работы с базой данных RuSyle
Обеспечивает подключение к БД и основные операции
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import json

class Database:
    """Класс для работы с базой данных SQLite"""
    
    def __init__(self, db_path: str = 'data/database.db'):
        """
        Инициализация подключения к базе данных
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Создает директорию для базы данных если её нет"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def get_connection(self):
        """Получить соединение с базой данных"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для работы со строками как со словарями
        return conn
    
    # ========== ИНИЦИАЛИЗАЦИЯ БАЗЫ ==========
    
    def initialize_database(self):
        """Инициализирует базу данных и создает таблицы"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Создание таблицы пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_developer BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Создание таблицы разработчиков/студий
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS developers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    studio_name TEXT NOT NULL,
                    description TEXT,
                    website TEXT,
                    logo_url TEXT,
                    founded_year INTEGER,
                    contact_email TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Создание таблицы игр
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    developer_id INTEGER,
                    genre TEXT,
                    platform TEXT,
                    release_date DATE,
                    description TEXT,
                    rating REAL DEFAULT 0,
                    image_url TEXT,
                    website TEXT,
                    steam_id TEXT,
                    status TEXT DEFAULT 'released', -- released, upcoming, beta, early_access
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (developer_id) REFERENCES developers (id)
                )
            ''')
            
            # Создание таблицы событий
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    game_id INTEGER,
                    event_date DATETIME NOT NULL,
                    end_date DATETIME,
                    location TEXT,
                    description TEXT,
                    event_type TEXT, -- presentation, tournament, stream, update, conference
                    organizer_id INTEGER,
                    is_online BOOLEAN DEFAULT 0,
                    registration_url TEXT,
                    image_url TEXT,
                    max_participants INTEGER,
                    current_participants INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'upcoming', -- upcoming, ongoing, finished, cancelled
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES games (id),
                    FOREIGN KEY (organizer_id) REFERENCES developers (id)
                )
            ''')
            
            # Создание таблицы подписок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    game_id INTEGER,
                    developer_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, game_id),
                    UNIQUE(user_id, developer_id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (game_id) REFERENCES games (id),
                    FOREIGN KEY (developer_id) REFERENCES developers (id)
                )
            ''')
            
            # Создание таблицы обновлений игр
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    version TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    release_date DATE,
                    patch_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
            ''')
            
            # Создание таблицы комментариев
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    game_id INTEGER,
                    event_id INTEGER,
                    content TEXT NOT NULL,
                    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (game_id) REFERENCES games (id),
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )
            ''')
            
            conn.commit()
            print("✅ База данных успешно инициализирована")
            
            # Добавление тестовых данных если таблицы пустые
            self.add_sample_data()
            
        except sqlite3.Error as e:
            print(f"❌ Ошибка при инициализации базы данных: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    # ========== ТЕСТОВЫЕ ДАННЫЕ ==========
    
    def add_sample_data(self):
        """Добавляет тестовые данные в базу"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Проверяем, есть ли уже данные
            cursor.execute("SELECT COUNT(*) FROM games")
            if cursor.fetchone()[0] > 0:
                print("📊 В базе уже есть данные, пропускаем добавление тестовых")
                return
            
            print("📝 Добавляем тестовые данные...")
            
            # Добавляем тестовых пользователей
            sample_users = [
                ('gamer123', 'gamer@example.com', 'hashed_password1', 0),
                ('dev_studio', 'studio@example.com', 'hashed_password2', 1),
                ('admin', 'admin@rusyle.ru', 'hashed_password3', 1)
            ]
            
            cursor.executemany('''
                INSERT INTO users (username, email, password_hash, is_developer)
                VALUES (?, ?, ?, ?)
            ''', sample_users)
            
            # Добавляем разработчиков
            sample_developers = [
                (2, 'Mundfish', 'Российская студия разработки игр', 'https://mundfish.com', 
                 'mundfish_logo.png', 2017, 'contact@mundfish.com'),
                (3, 'Battlestate Games', 'Разработчик хардкорных шутеров', 
                 'https://www.escapefromtarkov.com', 'bsg_logo.png', 2012, 'info@battlestategames.com')
            ]
            
            cursor.executemany('''
                INSERT INTO developers (user_id, studio_name, description, website, 
                                        logo_url, founded_year, contact_email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_developers)
            
            # Добавляем игры
            sample_games = [
                ('Atomic Heart', 1, 'Экшен/RPG', 'PC, PS5, Xbox Series X|S', 
                 '2023-02-21', 'Игра в жанре экшен от российской студии Mundfish', 
                 8.5, 'atomic_heart.jpg', 'https://mundfish.com', '668580', 'released'),
                ('Escape from Tarkov', 2, 'Хардкор-шутер', 'PC', 
                 '2017-07-27', 'Хардкорный шутер от российских разработчиков', 
                 9.0, 'tarkov.jpg', 'https://www.escapefromtarkov.com', '589380', 'released'),
                ('War Thunder', NULL, 'Симулятор/Экшен', 'PC, PS4, Xbox One', 
                 '2013-08-15', 'Военный симулятор с участием российской студии', 
                 8.0, 'war_thunder.jpg', 'https://warthunder.com', '236390', 'released'),
                ('Космические Рейнджеры HD', NULL, 'Стратегия/RPG', 'PC', 
                 '2013-12-12', 'Культовая российская космическая стратегия', 
                 9.5, 'rangers.jpg', 'https://www.katauri.com', '46400', 'released')
            ]
            
            cursor.executemany('''
                INSERT INTO games (title, developer_id, genre, platform, release_date, 
                                   description, rating, image_url, website, steam_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_games)
            
            # Добавляем события
            sample_events = [
                ('Презентация Atomic Heart 2', 1, '2024-03-15 19:00:00', '2024-03-15 21:00:00',
                 'Москва, Крокус Экспо', 'Анонс продолжения культовой игры', 
                 'presentation', 1, 0, 'https://register.example.com', 
                 'atomic_event.jpg', 500, 0, 'upcoming'),
                ('Турнир по Tarkov', 2, '2024-02-28 15:00:00', '2024-02-28 20:00:00',
                 'Онлайн', 'Киберспортивный турнир с призовым фондом', 
                 'tournament', 2, 1, 'https://tournament.tarkov.com', 
                 'tarkov_tournament.jpg', 100, 42, 'upcoming'),
                ('Выпуск крупного обновления War Thunder', 3, '2024-03-10 12:00:00', NULL,
                 'Онлайн', 'Добавление новой техники и карт',
                 'update', NULL, 1, NULL, 
                 'update_event.jpg', NULL, NULL, 'upcoming')
            ]
            
            cursor.executemany('''
                INSERT INTO events (title, game_id, event_date, end_date, location, 
                                   description, event_type, organizer_id, is_online, 
                                   registration_url, image_url, max_participants, 
                                   current_participants, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_events)
            
            # Добавляем обновления игр
            sample_updates = [
                (1, '1.2.0', 'Новые враги и локации', 
                 'Добавлены новые типы врагов и расширены существующие локации',
                 '2024-01-15', '- Новые типы врагов\n- Улучшенная графика\n- Исправление багов'),
                (2, '0.14.0', 'Новый контент и баланс', 
                 'Добавлено новое оружие и переработан баланс',
                 '2024-02-01', '- Новое оружие\n- Изменения баланса\n- Оптимизация производительности')
            ]
            
            cursor.executemany('''
                INSERT INTO game_updates (game_id, version, title, description, release_date, patch_notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_updates)
            
            conn.commit()
            print(f"✅ Добавлено тестовых данных: {len(sample_games)} игр, {len(sample_events)} событий")
            
        except sqlite3.Error as e:
            print(f"❌ Ошибка при добавлении тестовых данных: {e}")
        finally:
            if conn:
                conn.close()
    
    # ========== ОСНОВНЫЕ МЕТОДЫ ДЛЯ РАБОТЫ С ДАННЫМИ ==========
    
    def get_all_games(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Получить все игры с пагинацией"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT g.*, d.studio_name as developer_name, d.logo_url as developer_logo
                FROM games g
                LEFT JOIN developers d ON g.developer_id = d.id
                ORDER BY g.rating DESC, g.created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            games = [dict(row) for row in cursor.fetchall()]
            return games
            
        except sqlite3.Error as e:
            print(f"Ошибка при получении игр: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_game_by_id(self, game_id: int) -> Optional[Dict]:
        """Получить игру по ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT g.*, d.studio_name as developer_name, d.description as developer_description,
                       d.website as developer_website, d.logo_url as developer_logo
                FROM games g
                LEFT JOIN developers d ON g.developer_id = d.id
                WHERE g.id = ?
            ''', (game_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
        except sqlite3.Error as e:
            print(f"Ошибка при получении игры {game_id}: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_upcoming_events(self, limit: int = 10) -> List[Dict]:
        """Получить ближайшие события"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT e.*, g.title as game_title, g.image_url as game_image,
                       d.studio_name as organizer_name
                FROM events e
                LEFT JOIN games g ON e.game_id = g.id
                LEFT JOIN developers d ON e.organizer_id = d.id
                WHERE e.event_date >= datetime('now') 
                AND e.status = 'upcoming'
                ORDER BY e.event_date ASC
                LIMIT ?
            ''', (limit,))
            
            events = [dict(row) for row in cursor.fetchall()]
            return events
            
        except sqlite3.Error as e:
            print(f"Ошибка при получении событий: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def search_games(self, query: str, limit: int = 20) -> List[Dict]:
        """Поиск игр по названию или описанию"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT g.*, d.studio_name as developer_name
                FROM games g
                LEFT JOIN developers d ON g.developer_id = d.id
                WHERE g.title LIKE ? OR g.description LIKE ? OR g.genre LIKE ?
                ORDER BY g.rating DESC
                LIMIT ?
            ''', (search_pattern, search_pattern, search_pattern, limit))
            
            games = [dict(row) for row in cursor.fetchall()]
            return games
            
        except sqlite3.Error as e:
            print(f"Ошибка при поиске игр: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_games_by_genre(self, genre: str, limit: int = 20) -> List[Dict]:
        """Получить игры по жанру"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT g.*, d.studio_name as developer_name
                FROM games g
                LEFT JOIN developers d ON g.developer_id = d.id
                WHERE g.genre LIKE ?
                ORDER BY g.rating DESC
                LIMIT ?
            ''', (f"%{genre}%", limit))
            
            games = [dict(row) for row in cursor.fetchall()]
            return games
            
        except sqlite3.Error as e:
            print(f"Ошибка при получении игр по жанру {genre}: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def add_game(self, game_data: Dict) -> Optional[int]:
        """Добавить новую игру"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO games (title, developer_id, genre, platform, release_date,
                                   description, rating, image_url, website, steam_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_data.get('title'),
                game_data.get('developer_id'),
                game_data.get('genre'),
                game_data.get('platform'),
                game_data.get('release_date'),
                game_data.get('description'),
                game_data.get('rating', 0),
                game_data.get('image_url'),
                game_data.get('website'),
                game_data.get('steam_id'),
                game_data.get('status', 'upcoming')
            ))
            
            game_id = cursor.lastrowid
            conn.commit()
            return game_id
            
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении игры: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def add_event(self, event_data: Dict) -> Optional[int]:
        """Добавить новое событие"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (title, game_id, event_date, end_date, location,
                                   description, event_type, organizer_id, is_online,
                                   registration_url, image_url, max_participants,
                                   current_participants, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data.get('title'),
                event_data.get('game_id'),
                event_data.get('event_date'),
                event_data.get('end_date'),
                event_data.get('location'),
                event_data.get('description'),
                event_data.get('event_type'),
                event_data.get('organizer_id'),
                event_data.get('is_online', 0),
                event_data.get('registration_url'),
                event_data.get('image_url'),
                event_data.get('max_participants'),
                event_data.get('current_participants', 0),
                event_data.get('status', 'upcoming')
            ))
            
            event_id = cursor.lastrowid
            conn.commit()
            return event_id
            
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении события: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_game_updates(self, game_id: int) -> List[Dict]:
        """Получить обновления для игры"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM game_updates
                WHERE game_id = ?
                ORDER BY release_date DESC
            ''', (game_id,))
            
            updates = [dict(row) for row in cursor.fetchall()]
            return updates
            
        except sqlite3.Error as e:
            print(f"Ошибка при получении обновлений игры {game_id}: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_statistics(self) -> Dict:
        """Получить статистику платформы"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            stats = {}
            
            # Количество игр
            cursor.execute("SELECT COUNT(*) FROM games")
            stats['total_games'] = cursor.fetchone()[0]
            
            # Количество событий
            cursor.execute("SELECT COUNT(*) FROM events")
            stats['total_events'] = cursor.fetchone()[0]
            
            # Количество предстоящих событий
            cursor.execute("SELECT COUNT(*) FROM events WHERE event_date >= datetime('now')")
            stats['upcoming_events'] = cursor.fetchone()[0]
            
            # Количество разработчиков
            cursor.execute("SELECT COUNT(*) FROM developers")
            stats['total_developers'] = cursor.fetchone()[0]
            
            # Самые популярные жанры
            cursor.execute('''
                SELECT genre, COUNT(*) as count 
                FROM games 
                WHERE genre IS NOT NULL 
                GROUP BY genre 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            stats['top_genres'] = [dict(row) for row in cursor.fetchall()]
            
            # Последние добавленные игры
            cursor.execute('''
                SELECT title, rating, image_url 
                FROM games 
                ORDER BY created_at DESC 
                LIMIT 3
            ''')
            stats['recent_games'] = [dict(row) for row in cursor.fetchall()]
            
            return stats
            
        except sqlite3.Error as e:
            print(f"Ошибка при получении статистики: {e}")
            return {}
        finally:
            if conn:
                conn.close()
    
    def export_to_json(self, filename: str = 'data/backup.json'):
        """Экспортировать все данные в JSON файл"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            data = {}
            
            # Экспортируем все таблицы
            tables = ['games', 'events', 'developers', 'game_updates']
            
            for table in tables:
                cursor.execute(f'SELECT * FROM {table}')
                rows = cursor.fetchall()
                data[table] = [dict(row) for row in rows]
            
            # Сохраняем в файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"✅ Данные экспортированы в {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при экспорте данных: {e}")
            return False
        finally:
            if conn:
                conn.close()

# Создаем глобальный экземпляр базы данных
db = Database()

def init_database():
    """Инициализировать базу данных (функция для импорта)"""
    return db.initialize_database()

def get_database() -> Database:
    """Получить экземпляр базы данных"""
    return db

# Тестирование при прямом запуске
if __name__ == '__main__':
    print("🧪 Тестирование модуля базы данных...")
    
    # Инициализируем базу
    db.initialize_database()
    
    # Получаем статистику
    stats = db.get_statistics()
    print(f"\n📊 Статистика платформы:")
    print(f"  Игр: {stats.get('total_games', 0)}")
    print(f"  Событий: {stats.get('total_events', 0)}")
    print(f"  Предстоящих событий: {stats.get('upcoming_events', 0)}")
    print(f"  Разработчиков: {stats.get('total_developers', 0)}")
    
    # Получаем все игры
    games = db.get_all_games(limit=3)
    print(f"\n🎮 Последние игры ({len(games)}):")
    for game in games:
        print(f"  • {game['title']} - {game.get('developer_name', 'Неизвестно')}")
    
    # Получаем предстоящие события
    events = db.get_upcoming_events(limit=3)
    print(f"\n📅 Предстоящие события ({len(events)}):")
    for event in events:
        print(f"  • {event['title']} - {event['event_date']}")
    
    print("\n✅ Тестирование завершено успешно!")
