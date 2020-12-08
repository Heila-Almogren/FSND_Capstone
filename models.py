from sqlalchemy.sql import case
from flask_migrate import Migrate
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import os


SECRET_KEY = os.urandom(32)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# DEBUG = True

# db = SQLAlchemy()


# def setup_db(app):
#     app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://wbfklsphwlmduc:c40246534cba0576044ffeacac5477c7c1452e0b033bc515cfd762ef033965e3@ec2-50-19-247-157.compute-1.amazonaws.com:5432/djebui0b714jr'
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)


# def db_drop_and_create_all():
#     db.drop_all()
#     db.create_all()


# class Movie(db.Model):
#     __tablename__ = 'Movie'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)
#     release_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()


# class Actor(db.Model):
#     __tablename__ = 'Actor'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     age = db.Column(db.Integer)
#     gender = db.Column(db.String)

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()
