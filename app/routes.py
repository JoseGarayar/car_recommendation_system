from flask import render_template, redirect, url_for, flash, request, session
from flask_jwt_extended import create_access_token, jwt_required
from .models import User
from . import app, db, bcrypt

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity={'email': user.email})
            session['jwt_token'] = access_token
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')