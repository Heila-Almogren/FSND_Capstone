import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    """
    Returns:
        The list of all drinks in short representation
    """
    try:

        # Fetch all drinks
        drinks = Drink.query.all()

        return jsonify({
            'success': True,
            "drinks": [drink.short() for drink in drinks]
        })
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    """
    Returns:
        The list of all drinks in long representation
    """
    try:
        # Fetch all drinks
        drinks = Drink.query.all()
        print('drinks are')
        print(drinks)

        return jsonify({
            'success': True,
            "drinks": [drink.long()
                       for drink in drinks]
        })
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    """
    Returns:
        The object of newly created drink
    """
    try:
        # attributes of the new drink
        title = request.json['title']
        recipe = request.json['recipe']

        # Create the new drink with attributes
        nDrink = Drink(title=title, recipe=json.dumps(recipe))
        nDrink.insert()

        return jsonify({
            'success': True,
            'drinks': nDrink.long()
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('post:drinks')
def patch_drink(jwt, id):
    """
    Args
        The id of the drink to be edited
    Returns:
        The edited drink object
    """
    try:

        # Fetch new data
        body = request.get_json()
        ntitle = body.get('title', None)
        nrecipe = json.dumps(body.get('recipe', None))

        # Get drink
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if not ntitle == 'null':
            drink.title = ntitle
        if not nrecipe == 'null':
            drink.recipe = nrecipe

        # Update drink data
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
        })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('post:drinks')
def delete_drink(jwt, id):
    """
    Args
        The id of the drink to be deleted
    Returns:
        The id of the deleted drink
    """
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.delete()

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


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''


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
