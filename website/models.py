from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    packing_lists = db.relationship('PackingList', lazy=True)

class PackingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    target_weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gear = db.relationship('Gear', secondary='packing_list_gear')

class Gear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    temperature_rating = db.Column(db.Float)
    packing_lists = db.relationship('PackingList', secondary='packing_list_gear')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

packing_list_gear = db.Table(
    'packing_list_gear',
    db.Column('packing_list_id', db.Integer, db.ForeignKey('packing_list.id'), primary_key=True),
    db.Column('gear_id', db.Integer, db.ForeignKey('gear.id'), primary_key=True)
)