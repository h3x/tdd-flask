from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()

def create_app(script_info=None):
    app = Flask(__name__)

    # Set Config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)

    # Register blueprints
    from src.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint)

    from src.api.users import user_blueprint
    app.register_blueprint(user_blueprint)

    # Shell contect for flask cli
    @app.shell_context_processor
    def ctx():
        return { 'app': app, 'db':db }

    return app