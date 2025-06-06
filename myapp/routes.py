from flask import Blueprint, redirect, render_template, url_for,request,jsonify
from flask_login import current_user, login_user, logout_user,login_required
from .extensions import db
from .models import User

main = Blueprint('main', __name__)  

@main.route('/')
def home():
    return "hello world!"



@main.route('/register', methods=['POST'])
def register():
    # Accept JSON or form data
    data = request.get_json() if request.is_json else request.form

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not all([email, username, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(email=email, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return jsonify({'message': 'User registered successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json() if request.is_json else request.form
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        
        return jsonify({"message": "Logged in successfully","email":user.email,"username":user.username}), 200

    return jsonify({'error': 'Invalid credentials'}), 401



@main.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message" : "Logged out"}), 200

@main.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({"email": current_user.email, "username":current_user.username}), 200

@main.route('/users')
def index():
    users = User.query.all()
    users_list_html = [f"<li>{ user.username }</li>" for user in users]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/add/<username>')
def add_user(username):
    db.session.add(User(username=username))
    db.session.commit()
    return redirect(url_for("main.index"))