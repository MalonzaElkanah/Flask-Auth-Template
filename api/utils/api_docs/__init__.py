from flasgger import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from api.utils.api_docs.schemas import marshmallow_schemas
from api.utils.api_docs.responses import spec_responses
from api.utils.api_docs.examples import spec_examples
from api.utils.api_docs.parameters import spec_parameters


spec_info = dict({
    "description": "This is a documentation for a Space-Ya-Tech APIs.",
    "termsOfService": "http://127.0.0.1:5000/terms/",
    "contact": {
        "name": "API Support",
        "url": "https://elkanahmalonza.herokuapp.com/",
        "email": "elkanahmalonza@gmail.com"
    },
    "license": {
        "name": "MIT License",
        "url": "https://www.opensource.org/licenses/MIT"
    },
    "version": "1.0.0"
})


spec_components = dict({
    "schemas": {},
    "parameters": spec_parameters,
    "responses": spec_responses,
    "examples": spec_examples,

    "securitySchemes": {
        "bearer_token": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "TOKEN",
            "description": "Access Token for Authentication"
        },
        "bearer_refresh_token": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "TOKEN",
            "description": "Refresh Token for generating Access Token."
        }
    },
})


# Create an APISpec
spec = APISpec(
    title='Space-Ya-Tech APIs',
    version='1.0.0',
    openapi_version='3.0.2',
    info=spec_info,
    servers=[
        {
            "url": "http://127.0.0.1:5000/",
            "description": "Development server"
        },
    ],
    components=spec_components,
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


def spec_template(app):
    template = spec.to_flasgger(
        app,
        definitions=marshmallow_schemas,
        # paths=[]
    )

    return template
