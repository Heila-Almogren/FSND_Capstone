# from sqlalchemy.sql import case
# from flask_migrate import Migrate
import dateutil.parser
import babel
# from flask import Flask, render_template, request, Response, flash, redirect, url_for
# from flask_moment import Moment
import os
# from sqlalchemy import Column, String, Integer
# from flask_sqlalchemy import SQLAlchemy
# import json
# import datetime


SECRET_KEY = os.urandom(32)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
