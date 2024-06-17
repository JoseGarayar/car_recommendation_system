from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from models import User
from functools import wraps
import datetime

main = Blueprint('main', __name__)

def jwt_middleware():
    if 'access_token_cookie' in request.cookies:
        access_token = request.cookies.get('access_token_cookie')
        request.headers.environ['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

# Register the middleware
@main.before_request
def before_request():
    jwt_middleware()

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity={'email': user.email})
            response = redirect(url_for('main.dashboard'))
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@main.route('/')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')

@main.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = redirect(url_for('main.login'))
    unset_jwt_cookies(response)
    return response
