# Team-Rio-Flask
Team Rio Backend Written in Flask for the SpaceYaTech Project


## Table of Contents
- [Team-Rio-Flask](#team-rio-flask)
  - [Table of Contents](#table-of-contents)
  - [Product vision](#product-vision)
    - [Vision Abstract](#vision-abstract)
    - [Target Group](#target-group)
    - [Concrete Product Vision](#concrete-product-vision)
  - [Contribution Guide](#contribution-guide)
    - [New contributor guide](#new-contributor-guide)
    - [Getting started](#getting-started)
  - [Installation guide](#installation-guide)
    - [Dependacies Installation](#dependacies-installation)
    - [Database Initialization](#database-initialization)
  - [Testing and Running Guide](#testing-and-running-guide)
  - [Key Python Modules Used](#key-python-modules-used)
  - [Reference Resources](#reference-resources)

## Product vision

### Vision Abstract
As a user interested in technology space in Kenya, I should be able to use the application to find meaningful discussions on the tech ecosystem in Africa. The SpaceYaTech Forum should provide users with the opportunity to join communities, make posts, upvote other people's posts, comment on posts, downvote posts they don't like and report posts which don't abide by the community standards.

### Target Group
Young people interested in keeping in touch with what's happening in the tech space within Africa and other relevant topics which will boost their careers.

### Concrete Product Vision
FOR: young africans interested in technology discussions in Africa WHO: want to find opinions and news about various topics in Africa THE: Space Ya Tech IS A web application THAT: gives a platform to young people to interact on different technology matters UNLIKE: other existing products which already exist in the market OUR PRODUCT: is open source and developed by the community for the community addressing the pain points of the African tech ecosystem.


## Contribution Guide
Read our [Code of Conduct](https://github.com/SpaceyaTech/.github/blob/05d65ab42226f6479ab59a2209a9d128734ecbe6/CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

### New contributor guide
Here are some resources to help you get started
- [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)

### Getting started

#### Issues

##### Create a new issue

If you spot a problem with the project, search if a similar issue already exists. 
If a related issue doesn't exist, you can open a new issue 

##### Solve an issue

Scan through our existing issues to find one that interests you. 
You can narrow down the search using `labels` as filters. 
If you find an issue that you want to work on, comment on it to have it assigned to you;
and then you are welcome to open a PR with a fix

##### Make changes locally
1. Fork the repository.
- Using GitHub Desktop:
  - [Getting started with GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/getting-started-with-github-desktop) will guide you through setting up Desktop
  - Once Desktop is set up, you can use it to [fork the repo](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/cloning-and-forking-repositories-from-github-desktop)!

- Using the command line:
  - [Fork the repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) so that you can make your changes without affecting the original project until you're ready to merge them

2. Create a branch and start working on your changes!

#### Commit your update

Commit the changes once you are happy with them :zap:

#### Pull Request

When you're finished with the changes, create a pull request, also known as a PR.
- Don't forget to [link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if you are solving one
- Enable the checkbox to [allow maintainer edits](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so the branch can be updated for a merge
Once you submit your PR, a member of the team will review your changes. They may ask questions or request additional information
- You can make any other changes in your fork, then commit them to your branch to be part of the PR
- As you update your PR and apply changes, mark each conversation as [resolved](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request#resolving-conversations)
- If you run into any merge issues, checkout this [git tutorial](https://github.com/skills/resolve-merge-conflicts) to help you resolve merge conflicts and other issues.

#### Your PR has been merged!

Congratulations :tada::tada: The SpaceYaTech team thanks you :sparkles:

Once your PR is merged, your contributions will be publicly visible

## Installation Guide

### Dependacies Installation

- Installing the application locally requires 
	1. [Python 3.7+](https://www.python.org/downloads/release/python-393/) - download and install it.
	2. [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) - To create a virtual environment and activate it, run the following commands. 
	```bash
	$ python3 -m venv venv
	$ source venv/bin/activate
	```
- Install the project dependacies from requirements.txt by running the following command in shell: 
```bash
$ pip install -r requirements.txt 
```
- The project contains a `.env.sample` file at its root with the environment variables required to run the app. Copy the file and name it `.env`, populating it with the correct values.

### Database Initialization

- This Flask application needs a [PostgreSQL](https://www.postgresql.org/docs/current/tutorial-start.html) database to store data. Create a database for this project, get the Database Name, Port, host, username and password and add it to `.env` file as shown in `.env.sample` file.  
- Run the following commands to set-up(create tables for the project) the database using [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html): 
```bash
$ flask db init
$ flask db migrate -m 'set-up the db'
$ flask db upgrade
```
## Testing and Running Guide
1. To activate the development server run:
```bash
$ source FLASK_DEBUG=True
$ flask run
```
At this point, the development server should be accessible at _http://localhost:5000/_

2. Testing - To run all the tests:

```bash
$ python -m pytest -v
```

## Key Python Modules Used

* **Flask**: micro-framework for web application development which includes the following dependencies:
  * click: package for creating command-line interfaces (CLI)
  * itsdangerous: cryptographically sign data 
  * Jinja2: templating engine
  * MarkupSafe: escapes characters so text is safe to use in HTML and XML
  * Werkzeug: set of utilities for creating a Python application that can talk to a WSGI server
* **pytest**: framework for testing Python projects
* **Flask-SQLAlchemy** - ORM (Object Relational Mapper) for Flask
* **Flask-RESTful** - An extension for Flask that adds support for quickly building REST APIs.
* **psycopg2** - PostgreSQL database adapter for the Python programming language.
* **flake8** - static analysis tool

## Reference Resources
- [virtualenv](https://docs.python-guide.org/dev/virtualenvs/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)
- [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)
