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
    featured = Content.query.filter_by(page='home_featured').first()
    return render_template('home.html', content=content, featured=featured)

@main.route('/events')
def events():
    content = Content.query.filter_by(page='events').first()
    upcoming = Content.query.filter_by(page='events_upcoming').first()
    return render_template('events.html', content=content, upcoming=upcoming)

@main.route('/gallery')
def gallery():
    content = Content.query.filter_by(page='gallery').first()
    gallery_items = Content.query.filter_by(page='gallery_items').all()
    return render_template('gallery.html', content=content, gallery_items=gallery_items)

@main.route('/shop')
def shop():
    content = Content.query.filter_by(page='shop').first()
    products = Content.query.filter_by(page='shop_products').all()
    return render_template('shop.html', content=content, products=products)

@main.route('/downloads')
def downloads():
    content = Content.query.filter_by(page='downloads').first()
    downloads = Content.query.filter_by(page='download_items').all()
    return render_template('downloads.html', content=content, downloads=downloads)

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