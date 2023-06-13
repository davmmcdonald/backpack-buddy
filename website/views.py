from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import PackingList, Category, Gear
from . import db
from datetime import datetime
import string, random


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/create-list', methods=['GET', 'POST'])
@login_required
def create_list():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        date = request.form.get('date')
        distance = request.form.get('distance')
        target_weight = request.form.get('targetWeight')
        slug = generate_unique_slug(8)

        new_packing_list = PackingList(name=name, location=location, date=date, distance=distance, target_weight=target_weight, user_id=current_user.id, slug=slug)
        db.session.add(new_packing_list)
        db.session.commit()
        flash('List added successfully!', category='success')
        return redirect(url_for('views.dashboard'))

    return render_template('create-list.html', user=current_user)

@views.route('/list/<string:slug>', methods=['GET', 'POST'])
def list(slug):
    packing_list = PackingList.query.filter_by(slug=slug).first()
    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        weight = request.form.get('weight')
        temperature = request.form.get('temperature')

        new_gear = Gear(name=name, category_id=category, weight=weight, temperature_rating=temperature)
        packing_list.gear.append(new_gear)
        db.session.commit()
        return redirect(url_for('views.list', slug=slug))

    return render_template('list.html', packing_list=packing_list, categories=categories, user=current_user)

def generate_unique_slug(length):
    characters = string.ascii_letters + string.digits
    while True:
        slug = ''.join(random.choice(characters) for _ in range(length))
        existing_packing_list = PackingList.query.filter_by(slug=slug).first()
        if not existing_packing_list:
            return slug