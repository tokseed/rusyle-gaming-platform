"""
Модели данных для RuSyle
Определяет структуры данных для работы с приложением
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    """Модель пользователя"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    is_developer: bool = False
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_developer': self.is_developer,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

@dataclass
class Developer:
    """Модель разработчика/студии"""
    id: Optional[int] = None
    user_id: Optional[int] = None
    studio_name: str = ""
    description: str = ""
    website: str = ""
    logo_url: str = ""
    founded_year: Optional[int] = None
    contact_email: str = ""
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'studio_name': self.studio_name,
            'description': self.description,
            'website': self.website,
            'logo_url': self.logo_url,
            'founded_year': self.founded_year,
            'contact_email': self.contact_email
        }

@dataclass
class Game:
    """Модель игры"""
    id: Optional[int] = None
    title: str = ""
    developer_id: Optional[int] = None
    genre: str = ""
    platform: str = ""
    release_date: Optional[str] = None
    description: str = ""
    rating: float = 0.0
    image_url: str = ""
    website: str = ""
    steam_id: str = ""
    status: str = "upcoming"  # released, upcoming, beta, early_access
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Связанные данные (заполняются отдельно)
    developer: Optional[Developer] = None
    updates: List['GameUpdate'] = None
    events: List['Event'] = None
    
    def __post_init__(self):
        if self.updates is None:
            self.updates = []
        if self.events is None:
            self.events = []
    
    def to_dict(self, include_related: bool = False) -> dict:
        """Конвертировать в словарь"""
        data = {
            'id': self.id,
            'title': self.title,
            'developer_id': self.developer_id,
            'genre': self.genre,
            'platform': self.platform,
            'release_date': self.release_date,
            'description': self.description,
            'rating': self.rating,
            'image_url': self.image_url,
            'website': self.website,
            'steam_id': self.steam_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_related and self.developer:
            data['developer'] = self.developer.to_dict()
        
        return data

@dataclass
class Event:
    """Модель события"""
    id: Optional[int] = None
    title: str = ""
    game_id: Optional[int] = None
    event_date: str = ""
    end_date: Optional[str] = None
    location: str = ""
    description: str = ""
    event_type: str = ""  # presentation, tournament, stream, update, conference
    organizer_id: Optional[int] = None
    is_online: bool = False
    registration_url: str = ""
    image_url: str = ""
    max_participants: Optional[int] = None
    current_participants: int = 0
    status: str = "upcoming"  # upcoming, ongoing, finished, cancelled
    created_at: Optional[datetime] = None
    
    # Связанные данные
    game: Optional[Game] = None
    organizer: Optional[Developer] = None
    
    def to_dict(self, include_related: bool = False) -> dict:
        """Конвертировать в словарь"""
        data = {
            'id': self.id,
            'title': self.title,
            'game_id': self.game_id,
            'event_date': self.event_date,
            'end_date': self.end_date,
            'location': self.location,
            'description': self.description,
            'event_type': self.event_type,
            'organizer_id': self.organizer_id,
            'is_online': self.is_online,
            'registration_url': self.registration_url,
            'image_url': self.image_url,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_related:
            if self.game:
                data['game'] = self.game.to_dict()
            if self.organizer:
                data['organizer'] = self.organizer.to_dict()
        
        return data

@dataclass
class GameUpdate:
    """Модель обновления игры"""
    id: Optional[int] = None
    game_id: int = 0
    version: str = ""
    title: str = ""
    description: str = ""
    release_date: Optional[str] = None
    patch_notes: str = ""
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь"""
        return {
            'id': self.id,
            'game_id': self.game_id,
            'version': self.version,
            'title': self.title,
            'description': self.description,
            'release_date': self.release_date,
            'patch_notes': self.patch_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@dataclass
class Comment:
    """Модель комментария"""
    id: Optional[int] = None
    user_id: int = 0
    game_id: Optional[int] = None
    event_id: Optional[int] = None
    content: str = ""
    rating: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'game_id': self.game_id,
            'event_id': self.event_id,
            'content': self.content,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@dataclass
class Statistics:
    """Модель статистики платформы"""
    total_games: int = 0
    total_events: int = 0
    upcoming_events: int = 0
    total_developers: int = 0
    total_users: int = 0
    top_genres: List[dict] = None
    
    def __post_init__(self):
        if self.top_genres is None:
            self.top_genres = []
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь"""
        return {
            'total_games': self.total_games,
            'total_events': self.total_events,
            'upcoming_events': self.upcoming_events,
            'total_developers': self.total_developers,
            'total_users': self.total_users,
            'top_genres': self.top_genres
        }
