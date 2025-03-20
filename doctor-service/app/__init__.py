from flask import Flask
from app.database import db
from app.routes import doctor_blueprint
from flask_migrate import Migrate

def create_app():
    """Creates and configures the Flask application for Doctor Service."""
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize database and migrations
    db.init_app(app)
    Migrate(app, db)

    # Register Blueprint for doctor routes
    app.register_blueprint(doctor_blueprint, url_prefix="/doctors")

    return app

