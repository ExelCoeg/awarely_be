import os

from dotenv import load_dotenv
from flask import Flask

from myapp.models import User 

from .extensions import db, login_manager
from .routes import main


load_dotenv() 

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    #postgresql://awarely_postgresql_user:sLeviYCZm620wh3UQp6OwDpsXiuOAKmz@dpg-d0qielje5dus739jh6fg-a.oregon-postgres.render.com/awarely_postgresql
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    login_manager.init_app(app)
  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)


    return app