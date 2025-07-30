from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'dev-key-for-heva-dashboard'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)

    # Import and register routes
    from app.routes import main
    app.register_blueprint(main)

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
