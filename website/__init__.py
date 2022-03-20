from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy.engine import URL
import urllib


db = SQLAlchemy()
#DB_NAME = "database.db"
DB_NAME = 'Dra_Amanda'

def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = '123456'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    params = urllib.parse.quote_plus("Driver={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-QRED97F;DATABASE=Dra_Amanda;Trusted_Connection=yes")
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Paciente, Plano

    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')