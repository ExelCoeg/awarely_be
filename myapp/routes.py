from flask import Blueprint, redirect, render_template, url_for,request,jsonify
from flask_login import current_user, login_user, logout_user,login_required
from .extensions import db
from .models import User

main = Blueprint('main', __name__)  

@main.route('/')
def home():
    return "hello world!"



@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            return "Email already registered", 400

        new_user = User(email,username,password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.me'))  # or wherever you want to redirect

    return render_template('register.html')


@main.route('/login', methods=['GET' ,'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # use form instead of json
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.me'))  # Redirect to /me after login
        return "Invalid credentials", 401

    return render_template('login.html')  # Show login form


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