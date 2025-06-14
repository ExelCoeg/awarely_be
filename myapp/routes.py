from flask import Blueprint, redirect, url_for,request,jsonify
from flask_login import current_user, login_user, logout_user,login_required
from .extensions import db
from .models import User, Report
from datetime import datetime
from .models import ULTKSPCounseling, RMCounseling
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
        
        return jsonify({'message': 'Logged in successfully','email':user.email,'username':user.username}), 200

    return jsonify({'error': 'Invalid credentials'}), 401




@main.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message" : "Logged out"}), 200


@main.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({"email": current_user.email, "username":current_user.username, "is_admin": current_user.is_admin}), 200

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



@main.route('/api/reports', methods=['GET'])
@login_required
def get_reports():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = Report.query.order_by(Report.submitted_at.desc())
    total = query.count()
    reports = query.offset((page - 1) * limit).limit(limit).all()

    data = []
    for report in reports:
        data.append({
            'id': report.id,
            'contact': report.contact,
            'incident': report.incident,
            'assistance_needed': report.assistance_needed,
            'schedule_date': report.schedule_date.isoformat() if report.schedule_date else None,
            'schedule_time': report.schedule_time.strftime('%H:%M') if report.schedule_time else None,
        })

    return jsonify({
        'data': data,
        'total': total,
        'page': page,
        'limit': limit
    }), 201




@main.route('/report', methods=['POST'])
@login_required  # Jika ingin hanya user login yang bisa buat laporan
def create_report():
    data = request.get_json() if request.is_json else request.form

    contact = data.get('contact')
    incident = data.get('incident')
    assistance = data.get('assistance')  # 'Perlu' atau 'Tidak'
    schedule_date = data.get('date')  # format: yyyy-mm-dd
    schedule_time = data.get('time')  # format: HH:MM (24 jam)

    try:
        report = Report(
            contact=contact,
            incident=incident,
            assistance_needed=(assistance.lower() == 'perlu'),
            user_id=current_user.id,
            schedule_date=datetime.strptime(schedule_date, '%Y-%m-%d').date() if schedule_date else None,
            schedule_time=datetime.strptime(schedule_time, '%H:%M').time() if schedule_time else None
        )
        db.session.add(report)
        db.session.commit()

        return jsonify({'message': 'Laporan berhasil dikirim'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def handle_counseling_submission(model_class):
    data = request.get_json() if request.is_json else request.form

    contact = data.get('contact')
    counselor = data.get('counselor') 
    incident = data.get('incident')
    availability = data.get('availability') 
    schedule_date = data.get('date')
    schedule_time = data.get('time')


    try:
        report = model_class(
            contact=contact,
            counselor_name=counselor,
            incident=incident,
            availability= availability,
            user_id=current_user.id,
            schedule_date=datetime.strptime(schedule_date, '%Y-%m-%d').date() if schedule_date else None,
            schedule_time=datetime.strptime(schedule_time, '%H:%M').time() if schedule_time else None
        )
        db.session.add(report)
        db.session.commit()
        return jsonify({'message': 'Laporan berhasil dikirim'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/ultksp_counseling', methods=['POST'])
@login_required  # Jika ingin hanya user login yang bisa buat counseling
def create_ultksp_counseling():
    return handle_counseling_submission(ULTKSPCounseling)

@main.route('/rm_counseling', methods=['POST'])
@login_required  # Jika ingin hanya user login yang bisa buat counseling
def create_rm_counseling():
    return handle_counseling_submission(RMCounseling)
