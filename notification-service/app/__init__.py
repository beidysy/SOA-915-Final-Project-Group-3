from flask import Flask
from app.database import db
from app.routes import notification_blueprint
from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object("app.config.Config")

    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(notification_blueprint, url_prefix="/notifications")

    return app

