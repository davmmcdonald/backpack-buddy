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

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)