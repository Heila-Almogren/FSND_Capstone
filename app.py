
from flask import Flask, request, jsonify, abort, redirect, render_template, session, url_for, request, Response
from sqlalchemy import *
import json
import datetime
from flask_cors import CORS
from flask_migrate import Migrate
from auth import *
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from models import *


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


# Configuring Auth0 Credentials

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id='6GgkbfV45KVhO5kc6jq3Ot7itvpXW98j',
    client_secret='LX04ZbMM61z27IakrzoilR6Co5qpezk17iuYkBYZ_2et8Dx4iGKS1dCCZbEMWUyZ',
    api_base_url='https://heilafsnd.us.auth0.com',
    access_token_url='https://heilafsnd.us.auth0.com/oauth/token',
    authorize_url='https://heilafsnd.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


# Endpoints

@app.route('/')
def index():
    """
    Returns:
        The main page
    """
    return render_template('index.html')


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    """
    Returns:
        The list of all movies
    """
    try:

        movies = Movie.query.all()

        return jsonify({
            'success': True,
            "movies": [movie.id for movie in movies]
        })
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    """
    Returns:
        The list of all actors
    """
    try:
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            "actors": [actor.id for actor in actors]
        })
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(jwt):
    """
    Returns:
        The object of newly created movie
    """
    try:
        title = request.json['title']
        release_date = request.json['release_date']

        nMovie = Movie(title=title, release_date=release_date)
        nMovie.insert()

        return jsonify({
            'success': True,
            'movie': nMovie
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(jwt):
    """
    Returns:
        The object of newly created actor
    """
    try:

        name = request.json['name']
        age = request.json['age']
        gender = request.json['gender']

        nActor = Actor(name=name, age=age, gender=gender)
        nActor.insert()

        return jsonify({
            'success': True,
            'actor': nActor
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(jwt, id):
    """
    Args
        The id of the movie to be edited
    Returns:
        The edited movie object
    """
    try:
        body = request.get_json()
        ntitle = body.get('title', None)
        nrelease = body.get('release_date', None)

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if not ntitle == 'null':
            movie.title = ntitle
        if not nrelease == 'null':
            movie.release_date = nrelease

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actor(jwt, id):
    """
    Args
        The id of the actor to be edited
    Returns:
        The edited actor object
    """
    try:
        body = request.get_json()
        nname = body.get('name', None)
        nage = body.get('age', None)
        ngender = body.get('gender', None)

        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if not nname == 'null':
            actor.name = nname
        if not nage == 'null':
            actor.age = nage
        if not ngender == 'null':
            actor.gender = ngender

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, id):
    """
    Args
        The id of the movie to be deleted
    Returns:
        The id of the deleted movie
    """
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        movie.delete()

        return jsonify({
            'success': True,
            "delete": id
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, id):
    """
    Args
        The id of the movie to be deleted
    Returns:
        The id of the deleted movie
    """
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        actor.delete()

        return jsonify({
            'success': True,
            "delete": id
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    """

    returns:
        handling for 422 (unprocessable) Error

    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    """

    returns:
        handling for 404 (Not found) Error

    """

    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(400)
def Bad_request(error):
    """

    returns:
        handling for 400 (Bad request) Error

    """

    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    """

    returns:
        handling for 405 (method not allowed) Error

    """

    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def Server_error(error):
    """

    returns:
        handling for 500 (Server error) Error

    """

    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500


@app.errorhandler(403)
def forbidden(error):
    """

    returns:
        handling for 403 (forbidden) Error

    """

    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(409)
def Duplicate_resource(error):
    """

    returns:
        handling for 409 (Duplicate resource) Error

    """

    return jsonify({
        "success": False,
        "error": 409,
        "message": "Duplicate resource"
    }), 409


@app.errorhandler(AuthError)
def Auth_Error(error):
    """

    returns:
        handling for 401 (Authentication error) Error

    """

    return jsonify({
        "success": False,
        "error": 401,
        "message": "Authentication error"
    }), 401


if __name__ == '__main__':
    app.run()
