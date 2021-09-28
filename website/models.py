from enum import unique
from . import db
from datetime import datetime

class Money(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	value = db.Column(db.Float(), nullable=False)
	quantity = db.Column(db.Float(), nullable=False)

class Evolution(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime, default=datetime.now)
	value = db.Column(db.Float(), nullable=False, unique=True)

