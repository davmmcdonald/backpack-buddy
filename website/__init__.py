from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3vriT2@ZR6s#nZzUHBNvx9$h'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app