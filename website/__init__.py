from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3vriT2@ZR6s#nZzUHBNvx9$h'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .dashboard import dashboard

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/')

    from .models import User, PackingList, Gear, Category

    with app.app_context():
        db.create_all()
        predefined_categories = categories = [
            "Backpacking Gear",
            "Backcountry Kitchen",
            "Food & Water",
            "Clothing & Footwear",
            "Navigation",
            "Emergency & First Aid",
            "Health & Hygiene",
            "Tools & Repair Items",
            "Backpacking Extras",
            "Personal Items"
        ]
        for category_name in predefined_categories:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
        db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id));

    return app