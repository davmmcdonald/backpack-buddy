from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import PackingList, Category, Gear, packing_list_gear
from . import db
from datetime import datetime
import string, random, os, requests, json


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
    # image_folder = 'website/static/assets/card-images'
    # image_filenames = []
    # for filename in os.listdir(image_folder):
    #     if filename.endswith('.jpg') or filename.endswith('.png'):
    #         image_filenames.append(filename)

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
    total_weight = round(sum(item.weight for item in packing_list.gear) / 16, 1)

    weather_api_key = '5f62ab4b1dfb49de9a7223916230604'
    url = f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={packing_list.location}&aqi=no'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp_f = data['current']['temp_f']
        condition = data['current']['condition']['text'].lower()

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        weight = request.form.get('weight')
        temperature = request.form.get('temperature')

        new_gear = Gear(name=name, category_id=category, weight=weight, temperature_rating=temperature)
        packing_list.gear.append(new_gear)
        db.session.commit()
        return redirect(url_for('views.list', slug=slug))

    return render_template('list.html', packing_list=packing_list, categories=categories, total_weight=total_weight, temp_f=temp_f, condition=condition, user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/delete-list', methods=['POST'])
def delete_list():
    data = json.loads(request.data)
    packing_list = PackingList.query.get(data['listId'])
    if packing_list:
        if packing_list.user_id == current_user.id:
            db.session.delete(packing_list)
            db.session.commit()
    return jsonify({})

@views.route('/delete-gear', methods=['POST'])
def delete_gear():
    data = json.loads(request.data)
    packing_list = PackingList.query.get(data['listId'])
    gear = Gear.query.get(data['gearId'])
    if packing_list:
        if gear in packing_list.gear:
            packing_list.gear.remove(gear)
            db.session.commit()
    return jsonify({})

def generate_unique_slug(length):
    characters = string.ascii_letters + string.digits
    while True:
        slug = ''.join(random.choice(characters) for _ in range(length))
        existing_packing_list = PackingList.query.filter_by(slug=slug).first()
        if not existing_packing_list:
            return slug
    