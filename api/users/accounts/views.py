from flask import request, current_app, url_for
from flask_restful import Resource
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from api.users.accounts.schemas import AccountSchema, AccountUpdateSchema
from api.models import Account
from api.utils import db
from api.utils.views_utils import json_response, allowed_file

import os


class AccountViewAPI(Resource):

    @jwt_required()
    def get(self):
        """
        This endpoint lists all your user account
        ---
        tags:
          - users
          - accounts
        security:
          - bearer_token: []
        responses:
          '200':
              description: account list returned
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
                          $ref: '#/components/schemas/Account'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/accounts_lists_success'
          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
        """

        accounts = Account.query.filter_by(user_id=current_user.uuid)

        return json_response(
            status=200,
            message="Data fetched!",
            data=AccountSchema(many=True).dump(accounts)
        )

    @jwt_required()
    def post(self):
        """
        This endpoint is for creating a new user account.
        ---
        tags:
          - users
          - accounts
        security:
          - bearer_token: []
        requestBody:
          description: request to add a new user account
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AccountUpdate'
            application/octet-stream:
              schema:
                properties:
                  display_photo:
                    type: string
                    format: binary
        responses:
          '201':
            description: Account added Succefully
            content:
              application/json:
                schema:
                  type: object
                  properties:
                      message:
                        type: string
                      data:
                        $ref: '#/components/schemas/Account'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                example:
                  $ref: '#/components/examples/account_create_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            result = AccountSchema(
                exclude=["id", "date_created", "date_modified"]
            ).load(request.get_json())
        except ValidationError as error:

            return json_response(
                status=400,
                message="Please correct the errors",
                errors=error.messages
            )

        account = Account(**result, user_id=current_user.uuid)

        # check if the post request has the file part
        if 'display_photo' in request.files:
            file = request.files['display_photo']

            if file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        current_app.config['UPLOAD_FOLDER'],
                        filename
                    ))

                    account.display_photo = url_for(
                        'uploaded_file',
                        file_name=filename
                    )

        db.session.add(account)
        db.session.commit()

        account = Account.query.filter_by(name=result['name']).one_or_none()

        return json_response(
            status=201,
            data=AccountSchema().dump(account),
            message="Account Created."
        )


class AccountDetailViewAPI(Resource):

    @jwt_required()
    def get(self, account_id):
        """
        This endpoint returns detailed data of a user account
        ---
        tags:
          - users
          - accounts
        security:
          - bearer_token: []
        responses:
          '200':
              description: returned account details
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      data:
                        $ref: '#/components/schemas/Account'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/account_detail_success'
          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
          '404':
              $ref: '#/components/responses/NotFound'
        parameters:
          - $ref: '#/components/parameters/account_id'
        """

        account = Account.query.filter_by(
            uuid=account_id,
            user_id=current_user.uuid
        ).one_or_none()

        if account:

            return json_response(
                status=200,
                message="Data fetched!",
                data=AccountSchema().dump(account)
            )
        else:
            return json_response(
                status=404,
                message="Account not Found.",
                errors="Account not Found"
            )

    @jwt_required()
    def put(self, account_id):
        """
        This endpoint is for updating a user account.
        ---
        tags:
          - users
          - accounts
        security:
          - bearer_token: []
        requestBody:
          description: request to send update account
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AccountUpdate'
        responses:
          '200':
            description: Account updated Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/account_update_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '404':
              $ref: '#/components/responses/NotFound'
          '500':
            $ref: '#/components/responses/GeneralError'
        parameters:
          - $ref: '#/components/parameters/account_id'
        """

        try:
            result = AccountUpdateSchema().load(request.get_json())
        except ValidationError as error:

            return json_response(
                status=400,
                message="Please correct the errors",
                errors=error.messages
            )

        account = Account.query.filter_by(
            uuid=account_id,
            user_id=current_user.uuid
        ).one_or_none()

        if account:
            if account.name != result["name"]:
                account_exists = Account.query.filter_by(name=result["name"]).one_or_none()
                if account_exists:
                    return json_response(
                        status=400,
                        message="Please correct the errors",
                        errors={"name": ["name already exist."]}
                    )

                account.name = result["name"]

            account.bio_data = result["bio_data"]

            # check if the post request has the file part
            if 'display_photo' in request.files:
                file = request.files['display_photo']

                if file.filename != '':
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(
                            current_app.config['UPLOAD_FOLDER'],
                            filename
                        ))

                        account.display_photo = url_for(
                            'uploaded_file',
                            file_name=filename
                        )

            db.session.commit()

            return json_response(
                status=200,
                message="Account Updated!",
                data=AccountSchema().dump(account)
            )
        else:
            return json_response(
                status=404,
                message="Account not Found.",
                errors="Account not Found"
            )

    @jwt_required()
    def delete(self, account_id):
        """
        This endpoint is for deleting your user account.
        ---
        tags:
          - users
          - accounts
        security:
          - bearer_token: []
        responses:
          '200':
            description: Account deleted Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/account_delete_success'
          '400':
            $ref: '#/components/responses/TokenInvalid'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '404':
              $ref: '#/components/responses/NotFound'
          '500':
            $ref: '#/components/responses/GeneralError'
        parameters:
          - $ref: '#/components/parameters/account_id'
        """

        account = Account.query.filter_by(
            uuid=account_id,
            user_id=current_user.uuid
        ).one_or_none()

        if account:
            # TODO
            # Delete display_photo from uploads

            db.session.delete(account)
            db.session.commit()

            return json_response(
                status=200,
                message="Account Deleted!",
            )
        else:
            return json_response(
                status=404,
                message="Account not Found.",
                errors="Account not Found"
            )
