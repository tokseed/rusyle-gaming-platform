from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate, mail
from app.config import config


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)

    app.config.from_object(config.get(config_name, config['development']))

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Blueprints
    from app.auth import auth_bp
    from app.events import events_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Server error'}, 500

    return app

