from flask import Flask
from app.database import db
from app.routes import patient_blueprint
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(patient_blueprint, url_prefix="/patients")

    return app

