import os

from flask import Flask
from flask_cors import CORS

from myapp.models import User 

from .extensions import db, login_manager
from .routes import main


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    #postgresql://awarely_postgresql_user:sLeviYCZm620wh3UQp6OwDpsXiuOAKmz@dpg-d0qielje5dus739jh6fg-a.oregon-postgres.render.com/awarely_postgresql
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    login_manager.init_app(app)
  
    CORS(app, supports_credentials=True,origins=["http://127.0.0.1:5500","https://awarely-black.vercel.app"])
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)


    return app