from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from api.users.roles.schemas import RoleSchema
from api.models import Role
from api.utils import db
from api.utils.views_utils import role_required, json_response


class RolesViewAPI(Resource):

    @jwt_required()
    @role_required(['Admin', 'SuperAdmin'])
    def get(self):
        """
        This endpoint lists all roles in application
        ---
        tags:
          - users
          - admin
          - roles
        security:
          - bearer_token: []
        responses:
          '200':
              description: role list returned
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      data:
                        type: array
                        items:
                          $ref: '#/components/schemas/Role'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/role_lists_success'
          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
          '403':
              $ref: '#/components/responses/AccessDenied'
        """

        roles = Role.query.all()

        return json_response(
            status=200,
            message="Data fetched!",
            data=RoleSchema(many=True, exclude=["users"]).dump(roles)
        )

    @jwt_required()
    @role_required(['SuperAdmin'])
    def post(self):
        """
        This endpoint is for creating user role.
        ---
        tags:
          - users
          - admin
          - roles
        security:
          - bearer_token: []
        requestBody:
          description: request to send role name
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
        responses:
          '201':
            description: Role added Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/role_create_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '403':
            $ref: '#/components/responses/AccessDenied'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            result = RoleSchema(exclude=["users", "id"]).load(request.get_json())
        except ValidationError as error:

            return json_response(
                status=400,
                message="Please correct the errors",
                errors=error.messages
            )

        role = Role(**result)

        db.session.add(role)
        db.session.commit()

        role = Role.query.filter_by(name=result['name']).one_or_none()

        return json_response(
            status=201,
            data=RoleSchema().dump(role),
            message="Role Created."
        )


class RolesDetailViewAPI(Resource):

    @jwt_required()
    @role_required(['Admin', 'SuperAdmin'])
    def get(self, role_id):
        """
        This endpoint returns detailed data of a role
        ---
        tags:
          - users
          - admin
          - roles
        security:
          - bearer_token: []
        responses:
          '200':
              description: returned role details
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      data:
                        $ref: '#/components/schemas/RoleDetail'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/role_detail_success'
          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
          '403':
              $ref: '#/components/responses/AccessDenied'
          '404':
              $ref: '#/components/responses/NotFound'
        parameters:
          - $ref: '#/components/parameters/role_id'
        """

        role = Role.query.filter_by(uuid=role_id).one_or_none()

        if role:

            return json_response(
                status=200,
                message="Data fetched!",
                data=RoleSchema().dump(role)
            )
        else:
            return json_response(
                status=404,
                message="Role not Found.",
                errors="Role not Found"
            )

    @jwt_required()
    @role_required(['SuperAdmin'])
    def put(self, role_id):
        """
        This endpoint is for updating user role.
        ---
        tags:
          - users
          - admin
          - roles
        security:
          - bearer_token: []
        requestBody:
          description: request to send update role name
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
        responses:
          '200':
            description: Role updated Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/role_update_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '403':
            $ref: '#/components/responses/AccessDenied'
          '404':
              $ref: '#/components/responses/NotFound'
          '500':
            $ref: '#/components/responses/GeneralError'
        parameters:
          - $ref: '#/components/parameters/role_id'
        """

        try:
            result = RoleSchema(exclude=["users", "id"]).load(request.get_json())
        except ValidationError as error:

            return json_response(
                status=400,
                message="Please correct the errors",
                errors=error.messages
            )

        role = Role.query.filter_by(uuid=role_id).one_or_none()

        if role:
            role.name = result["name"]
            db.session.commit()

            return json_response(
                status=200,
                message="Role Updated!",
                data=RoleSchema().dump(role)
            )
        else:
            return json_response(
                status=404,
                message="Role not Found.",
                errors="Role not Found"
            )

    @jwt_required()
    @role_required(['SuperAdmin'])
    def delete(self, role_id):
        """
        This endpoint is for deleting user role.
        ---
        tags:
          - users
          - admin
          - roles
        security:
          - bearer_token: []
        responses:
          '200':
            description: Role deleted Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/role_delete_success'
          '400':
            $ref: '#/components/responses/TokenInvalid'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '403':
            $ref: '#/components/responses/AccessDenied'
          '404':
              $ref: '#/components/responses/NotFound'
          '500':
            $ref: '#/components/responses/GeneralError'
        parameters:
          - $ref: '#/components/parameters/role_id'
        """

        role = Role.query.filter_by(uuid=role_id).one_or_none()

        if role:
            db.session.delete(role)
            db.session.commit()

            return json_response(
                status=200,
                message="Role Deleted!",
            )
        else:
            return json_response(
                status=404,
                message="Role not Found.",
                errors="Role not Found"
            )
