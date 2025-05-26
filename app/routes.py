from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Content
from app import db, admin
from flask_admin.contrib.sqla import ModelView

main = Blueprint('main', __name__)

@main.route('/')
def home():
    content = Content.query.filter_by(page='home').first()
    return render_template('home.html', content=content)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))
        
        flash('Please check your login details and try again.')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Add admin views
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Content, db.session))