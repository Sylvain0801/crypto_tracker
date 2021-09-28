from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'crypto.db'

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SECRET_KEY'] = b'\x90M\xf4\x8e\x1fI\x95\xa9u\xf5\xf5\x88l g\x1f'
	db.init_app(app)

	from .views import views

	app.register_blueprint(views, url_prefix="/")

	from .models import Money, Evolution

	create_database(app)

	return app

def create_database(app):
	if not path.exists('website/' + DB_NAME):
		db.create_all(app=app)
