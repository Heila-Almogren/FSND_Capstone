# Casting Agency

#### Casting Agency API is used to store data about different movies and actors and enables cast team to access and edit those data based on their privilages. For example, while a casting assistant can view the list of all movies and actors, a director -for example- can edit/update any information if neccessary, and the executive producer can have a full access to view, add edit or delete any movie or actor.

## Accessing the environemnt

#### The production environment:

You can access the deployed version on the URL (https://heilas-casting-agency.herokuapp.com/)

#### The local/development environment:

first of all, you have to install the required dependencies:

1- navigate to the root folder

2- run `pip install requirements.txt` (or pip3).

3- After that you'll be able to run the application:<br />
` export FLASK_APP=app.py` <br />
`FLASK_ENV=development` <br />
`FLASK_DEBUG=true `
`flask run `

### Roles and privilages ([RBAC Controls](https://auth0.com/docs/authorization/rbac))

Access of reading, editing and writing to the database is restricted to specific roles. Those roles are:

#### Casting Assistant:

- GET /movies
- GET /actors

#### Casting Director:

- GET /movies
- GET /actors
- POST /actors
- PATCH /movies
- PATCH /actors
- DELETE /actors

#### Executive Producer:

- GET /movies
- GET /actors
- POST /movies
- POST /actors
- PATCH /movies
- PATCH /actors
- DELETE /movies
- DELETE /actors

## API Reference

### GET /movies

- returns a success flag, and the list of movies' IDs.
- example:
  generate and store a jwt token in variable `TOKEN` for an assistant account, then send the GET request:

`curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://heilas-casting-agency.herokuapp.com/movies `

### GET /actors

- returns a success flag, and the list of actors' IDs.

- example:
  generate and store a jwt token in variable `TOKEN` for an assistant account, then send the GET request:

`curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://heilas-casting-agency.herokuapp.com/actors `

### POST /movies

- adds a new movie to the database.
- example:
  generate and store a jwt token in variable `TOKEN` for an executive account, then send the POST request:

`curl -X POST -d ' {"title" : "mission impossible","realease_date" : "19/12/2020"}' -H 'Authorization: Bearer ${TOKEN}' http://heilas-casting-agency.herokuapp.com/movies `

### POST /actors

- adds a new actor to the database.
- example:
  generate and store a jwt token in variable `TOKEN` for a director account, then send the POST request:

`curl -X POST -d ' { "name" : "John", "age" : "22", "gender" : "male"}' -H 'Authorization: Bearer ${TOKEN}' http://heilas-casting-agency.herokuapp.com/movies `

### PATCH /movies

- Edits the data of a movie object in the database.
- example:
  generate and store a jwt token in variable `TOKEN` for an director account, then send the POST request:

`curl -X PATCH -d ' {"title" : "newer movie", "realease_date" : "2020-12-20"}' -H 'Authorization: Bearer ${TOKEN}' http://heilas-casting-agency.herokuapp.com/movies/1 `

### PATCH /actors

- Edits the data of an actor object in the database.
- example:
  generate and store a jwt token in variable `TOKEN` for a director account, then send the POST request:

`curl -X PATCH -d ' { "name" : "Newer John", "age" : "23", "gender" : "male"}' -H 'Authorization: Bearer ${TOKEN}' http://heilas-casting-agency.herokuapp.com/actors/1`

### DELETE /movies

- Deletes a movie from the database.
- Takes movie ID as an argument.
- Example:
  generate and store a jwt token in variable `TOKEN` for an director account, then send the POST request:

`curl -X DELETE -H 'Authorization: Bearer ${TOKEN}' http://heilas-casting-agency.herokuapp.com/movies/1 `

### DELETE /actors

- Deletes a movie from the database.
- Takes actor ID as an argument.
- Example:
  generate and store a jwt token in variable `TOKEN` for a director account, then send the POST request:

`curl -X DELETE -H 'Authorization: Bearer ${TOKEN}' http://heilas-casting-agency.herokuapp.com/actors/1`

### Errors

#### 404: Not Found:

Means that the resource is currently unavailable and can't be found in the server.

#### 422: Unprocessable:

Means that request is understood by the server, however for some reason it cannot be processed.

#### 400: Bad request:

Means that the request cannot be processed by the server due to a client side problem, such as syntax or invalid request.

#### 405: method not allowed:

Means that the requested method is not allowed to processed to the specified resource.

#### 500: Server error:

Means that the requested method could not be processed due to a server error problem.

## Tests

You can run the API test using Postman by importing the collection `Casting_Agency.postman_collection.json`.
