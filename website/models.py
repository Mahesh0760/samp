from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Model for storing searches in db
class TrendingSearches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Model for user sign-in/sign-up data
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, Primary_key=True)
    email_id = db.Column(db.String(100), Unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))


# Model for News Data
class NewsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(500))
    country = db.Column(db.String(500), Unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(500))
    description = db.Column(db.String(1500))
    link = db.Cloumn(db.String(200), Unique=True)
