# Flask API - AUTH Template


## Table of Contents
  - [Features](#features)
    - [Implemented](#implemented)
    - [Todo](#todo)
  - [Installation guide](#installation-guide)
    - [Dependacies Installation](#dependacies-installation)
    - [Database Initialization](#database-initialization)
  - [Testing and Running Guide](#testing-and-running-guide)
  - [API Documentation](#api-documentation)
  - [Key Python Modules Used](#key-python-modules-used)
  - [Reference Resources](#reference-resources)


## Features
### Implemented
1. create user
2. Confirm Email
3. Resend Email Confirmation link
4. Login (get refresh token and access token)
5. Get new Access Token from Refresh Token
6. Revoke tokens
7. change password
8. forgot password

9. CRUD Roles (Admin)
10. List, Read, Delete Users (Admin)

### Todo
- User Activity Logs
- login with socials (google, fb, twitter, etc)
- Phone SMS login
- PIN Auth
- Finger-print Auth
- 2 Way Authentication
- Face Recognition auth


## Installation Guide

### Dependacies Installation

- Installing the application locally requires 
	1. [Python 3.7+](https://www.python.org/downloads/release/python-393/) - download and install it.
	2. [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) - To create a virtual environment and activate it, run the following commands. 
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```
- Install the project dependacies from requirements.txt by running the following command in shell: 
```bash
pip install -r requirements.txt 
```
- The project contains a `.env.sample` file at its root with the environment variables required to run the app. Copy the file and name it `.env`, populating it with the correct values.

### Database Initialization

- This Flask application needs a [PostgreSQL](https://www.postgresql.org/docs/current/tutorial-start.html) database to store data. Create a database for this project, get the Database Name, Port, host, username and password and add it to `.env` file as shown in `.env.sample` file.  
- Run the following commands to set-up(create tables for the project) the database using [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html): 
```bash
flask db init
flask db migrate -m 'set-up the db'
flask db upgrade
```
- If this is your first time setting up, you will need initial data seeded to your database. Run the following command to-do so:
```bash
flask seed
```

## Testing and Running Guide
1. To activate the development server run:
```bash
export FLASK_DEBUG=True
flask run
```
At this point, the development server should be accessible at _http://localhost:5000/_

2. Testing - To run all the tests:

```bash
python -m pytest -v
```

## API Documentation
- **SwaggerUI Docs:** You can access, visualize and interact with your API resources via [http://localhost:5000/apidocs](http://localhost:5000/apidocs)
- **Postman API Collection:** You can access postman collection in [postman_collection.json](postman_collection.json)
- **OpenAPI Specification Docs:** [http://127.0.0.1:5000/apispec_1.json](http://127.0.0.1:5000/apispec_1.json)


## Key Python Modules Used

* **Flask**: micro-framework for web application development which includes the following dependencies:
  * click: package for creating command-line interfaces (CLI)
  * itsdangerous: cryptographically sign data 
  * Jinja2: templating engine
  * MarkupSafe: escapes characters so text is safe to use in HTML and XML
  * Werkzeug: set of utilities for creating a Python application that can talk to a WSGI server
* **pytest**: framework for testing Python projects
* **Flask-SQLAlchemy** - ORM (Object Relational Mapper) for Flask
* **Flask-Migrate** - An extension that handles SQLAlchemy database migrations for Flask applications using Alembic. 
* **Flask-RESTful** - An extension for Flask that adds support for quickly building REST APIs.
* **Marshmallow** - A framework for Object/Model Validation, serialization and deserialization.
* **Flask-JWT-Extended** - An extension for managing JSON Web Tokens.
* **psycopg2** - PostgreSQL database adapter for the Python programming language.
* **flasgger**, **apispec**  - a Flask extension to extract OpenAPI-Specification from all Flask views registered in your API.
* **flake8** - static analysis tool

## Reference Resources
- [virtualenv](https://docs.python-guide.org/dev/virtualenvs/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)
- [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) 
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [Flasgger](https://pypi.org/project/flasgger/)
