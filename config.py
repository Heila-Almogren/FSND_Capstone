from sqlalchemy.sql import case
from flask_migrate import Migrate
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json


SECRET_KEY = os.urandom(32)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Configuring Environment

ENV = 'dev'

if ENV == 'dev':
    BEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/agency'
else:
    BEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://wbfklsphwlmduc:c40246534cba0576044ffeacac5477c7c1452e0b033bc515cfd762ef033965e3@ec2-50-19-247-157.compute-1.amazonaws.com:5432/djebui0b714jr'

SQLALCHEMY_TRACK_MODIFICATIONS = False
