"""
Основное приложение RuSyle Gaming Platform
"""
from flask import Flask, render_template, jsonify, send_from_directory
import os
import sqlite3
from datetime import datetime

app = Flask(__name__, 
    static_folder='src/assets',
    template_folder='templates'
)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-123')
app.config['DATABASE'] = 'data/database.db'
app.config['UPLOAD_FOLDER'] = 'src/assets/images'

def check_database():
    """Проверка и отладка базы данных"""
    if not os.path.exists(app.config['DATABASE']):
        print("📊 База данных не существует, будет создана")
        return
    
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    try:
        # Проверить какие таблицы существуют
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        print(f"\n📊 Найдено таблиц в базе: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Проверить структуру games если таблица существует
        if any('games' in t[0].lower() for t in tables):
            c.execute("PRAGMA table_info(games)")
            columns = c.fetchall()
            print(f"\n📋 Структура таблицы games ({len(columns)} колонок):")
            for col in columns:
                print(f"  {col[0]}: {col[1]} ({col[2]})")
    except Exception as e:
        print(f"⚠️ Ошибка при проверке базы: {e}")
    finally:
        conn.close()

def init_db():
    """Инициализация базы данных"""
    os.makedirs('data', exist_ok=True)
    
    # Удаляем старую базу если есть проблемы
    if os.path.exists(app.config['DATABASE']):
        print("♻️  Пересоздаем базу данных...")
        os.remove(app.config['DATABASE'])
    
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    print("📁 Создаем таблицы...")
    
    # Создание таблиц
    c.execute('''
        CREATE TABLE games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            developer TEXT,
            genre TEXT,
            release_date DATE,
            description TEXT,
            rating REAL DEFAULT 0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            game_id INTEGER,
            event_date DATETIME,
            location TEXT,
            description TEXT,
            organizer TEXT,
            event_type TEXT,
            is_online BOOLEAN DEFAULT 0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    ''')
    
    # Добавление тестовых данных
    print("📝 Добавляем тестовые данные...")
    
    sample_games = [
        ('Atomic Heart', 'Mundfish', 'Экшен/RPG', '2023-02-21', 
         'Игра в жанре экшен от российской студии Mundfish', 8.5, 
         'atomic_heart.jpg'),
        ('Escape from Tarkov', 'Battlestate Games', 'Хардкор-шутер', '2017-07-27', 
         'Хардкорный шутер от российских разработчиков', 9.0, 
         'tarkov.jpg'),
        ('War Thunder', 'Gaijin Entertainment', 'Симулятор/Экшен', '2013-08-15', 
         'Военный симулятор с участием российской студии', 8.0, 
         'war_thunder.jpg')
    ]
    
    # ПРАВИЛЬНЫЙ INSERT - указываем конкретные колонки
    c.executemany('''
        INSERT INTO games (title, developer, genre, release_date, description, rating, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_games)
    
    sample_events = [
        ('Презентация Atomic Heart 2', 1, '2024-03-15 19:00:00', 
         'Москва, Крокус Экспо', 'Анонс продолжения культовой игры', 
         'Mundfish', 'Презентация', 0, 'atomic_event.jpg'),
        ('Турнир по Tarkov', 2, '2024-02-28 15:00:00', 
         'Онлайн', 'Киберспортивный турнир с призовым фондом', 
         'Battlestate Games', 'Турнир', 1, 'tarkov_tournament.jpg')
    ]
    
    c.executemany('''
        INSERT INTO events (title, game_id, event_date, location, description, 
                           organizer, event_type, is_online, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_events)
    
    conn.commit()
    
    # Проверим что добавилось
    c.execute("SELECT COUNT(*) FROM games")
    game_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM events")
    event_count = c.fetchone()[0]
    
    conn.close()
    
    print(f"✅ База данных инициализирована: {game_count} игр, {event_count} событий")

# ... остальные маршруты без изменений ...

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Запуск RuSyle Gaming Platform")
    print("=" * 60)
    
    check_database()  # Проверить текущее состояние
    init_db()         # Инициализировать/пересоздать базу
    
    print("\n🌐 Сервер запущен по адресу: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
