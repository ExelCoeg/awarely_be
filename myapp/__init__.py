import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from myapp.models import User 

from .extensions import db, login_manager
from .routes import main

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    login_manager.init_app(app)
  
    CORS(app, supports_credentials=True,origins=["http://127.0.0.1:5500","https://awarely-black.vercel.app"])
    migrate.init_app(app, db)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.config.update(
        SESSION_COOKIE_SECURE=True,        
        SESSION_COOKIE_SAMESITE='None',    
    )
    with app.app_context():
        if not User.query.filter_by(is_admin=True).first():

            admin_email = os.environ.get("ADMIN_EMAIL")
            admin_username = os.environ.get("ADMIN_USERNAME")
            admin_password = os.environ.get("ADMIN_PASSWORD")

            admin = User(
                email=admin_email,
                username=admin_username,
                password=admin_password,
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()


    return app