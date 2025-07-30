from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the database
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')

    # Configuration
    app.config['SECRET_KEY'] = 'dev-key-for-heva-dashboard'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)
    migrate.init_app(app, db)

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

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
