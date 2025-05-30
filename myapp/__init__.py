import os

from flask import Flask 

from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    #postgresql://awarely_postgresql_user:sLeviYCZm620wh3UQp6OwDpsXiuOAKmz@dpg-d0qielje5dus739jh6fg-a.oregon-postgres.render.com/awarely_postgresql

    db.init_app(app)

    app.register_blueprint(main)

    return app