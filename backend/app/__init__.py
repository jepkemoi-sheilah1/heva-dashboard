from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize the database
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend', instance_relative_config=True)

    # Configuration
    app.config['SECRET_KEY'] = 'dev-key-for-heva-dashboard'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS for all domains on all routes
    CORS(app)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to register them with SQLAlchemy
    from app import models

    # Import and register routes
    from app.routes import main
    app.register_blueprint(main)

    # Serve frontend index.html at root
    @app.route('/')
    def serve_index():
        if app.template_folder is None:
            return "Template folder not set", 500
        return send_from_directory(app.template_folder, 'index.html')

    # Serve static files from frontend/static
    @app.route('/static/<path:path>')
    def serve_static(path):
        if app.static_folder is None:
            return "Static folder not set", 500
        return send_from_directory(app.static_folder, path)

    return app
