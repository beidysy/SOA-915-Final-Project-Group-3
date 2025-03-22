from flask import Flask
from app.database import db
from app.routes import doctor_blueprint
from flask_migrate import Migrate

def create_app(test_config=None):
    """Creates and configures the Flask application for Doctor Service."""
    app = Flask(__name__)

    # Use custom test config if provided, otherwise load default config
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object("app.config.Config")

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(doctor_blueprint, url_prefix="/doctors")

    return app
