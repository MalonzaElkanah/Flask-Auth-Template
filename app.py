import click
import uuid

from flask.cli import with_appcontext
from flask_restful import Api
from flasgger import Swagger

from api.utils import create_app, db, jwt
from api.utils.application_data import roles
from api.utils.api_docs import spec_template
from api.urls import api_urls
from api.models import Role, User, TokenBlocklist


app = create_app('config.Config', name="Main")

# Register Urls
api = Api(app)
api_urls(api)


# CLI Commands
def seed():
    print("Seeding Data: initiated adding roles...")
    for role in roles:
        _role = Role.query.filter_by(name=role).one_or_none()
        print(f"Seeding Data: adding {role} role...")
        if not _role:
            role = Role(name=role, uuid=uuid.uuid1())
            db.session.add(role)
            db.session.commit()

    print("Seeding Data: adding roles completed.")


@click.command('seed')
@with_appcontext
def seed_db_command():
    """
    Populate db with initial data.
    For Instance: Roles
    """

    confirm = input(
        "\n\nAre you sure you want to seed "
        "role data to the db? (Yes/No):"
    )
    if not confirm.lower().strip() in ["y", "yes"]:
        return "\n\n\t\033[31mAborted!\033[00m\n\n"

    click.echo('Initialized database seeding...')
    seed()


# Register cli commands
app.cli.add_command(seed_db_command)


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    print(f"userrrrrr: {user}")
    return user


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(uuid=identity).one_or_none()


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


# API Swagger Docs
app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3
}
swagger = Swagger(app, template=spec_template(app))
