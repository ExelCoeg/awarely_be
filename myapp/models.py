from .extensions import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr


class User(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password_hash = db.Column(db.String(512),nullable=False)
    
    def __init__(self,email,username,password):
        self.email = email
        self.username=username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key untuk mengaitkan laporan dengan pengguna (jika ada)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('reports', lazy=True))

    contact = db.Column(db.String(20), nullable=False)  # WhatsApp/Line
    incident = db.Column(db.Text, nullable=False)       # Cerita kejadian
    assistance_needed = db.Column(db.Boolean, nullable=False)  # Perlu bantuan?
    
    schedule_date = db.Column(db.Date, nullable=True)  # Jadwal tanggal
    schedule_time = db.Column(db.Time, nullable=True)  # Jadwal jam

    submitted_at = db.Column(db.DateTime, default=db.func.now())  # Waktu submit


class BaseCounseling(db.Model):
    __abstract__ = True  

    
    id = db.Column(db.Integer, primary_key=True)


    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', backref=db.backref(cls.__tablename__, lazy=True))

    counselor_name = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(20), nullable=False)
    incident = db.Column(db.Text, nullable=False)
    availability = db.Column(db.String(10), nullable=False)
    schedule_date = db.Column(db.Date, nullable=True)
    schedule_time = db.Column(db.Time, nullable=True)
    submitted_at = db.Column(db.DateTime, default=db.func.now())

class ULTKSPCounseling(BaseCounseling):
    __tablename__ = 'ultksp_counselings'

class RMCounseling(BaseCounseling):
    __tablename__ = 'rm_counselings'