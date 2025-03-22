from flask import Flask
from app.database import db
from app.routes import patient_blueprint
from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__)

    # Load default config
    app.config.from_object("app.config.Config")

    # Override with test config if provided
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(patient_blueprint, url_prefix="/patients")

    return app

