from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)

from api.utils import db, token

import uuid
import datetime as dt


# many to many users to roles association table
user_role = db.Table(
    "user_role",
    db.Column("user_id", db.String(36), db.ForeignKey("user.uuid")),
    db.Column("role_id", db.String(36), db.ForeignKey("role.uuid")),
    db.Column("date_added", db.DateTime, default=dt.datetime.utcnow),
    db.UniqueConstraint("user_id", "role_id"),
)


class Role(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=uuid.uuid1())
    name = db.Column(db.String(64), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=dt.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=dt.datetime.utcnow)

    users = db.relationship(
        "User",
        secondary="user_role",
        lazy="dynamic",
        order_by="desc(user_role.c.date_added)",
        backref=db.backref("my_roles", lazy="dynamic"),
    )

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    uuid = db.Column(db.String(40), primary_key=True, default=uuid.uuid1())
    username = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, index=True, unique=True)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    is_email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirm_token = db.Column(db.String, nullable=True)
    auth_token = db.Column(db.String, nullable=True)
    number_of_verification_requests = db.Column(db.Integer, nullable=True, default=0)

    date_created = db.Column(db.DateTime, default=dt.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=dt.datetime.utcnow)

    roles = db.relationship("Role", secondary="user_role", backref="my_users", viewonly=True)
    accounts = db.relationship(
        "Account",
        backref="user",
        lazy="dynamic",
        cascade="save-update, merge, refresh-expire, expunge",
        order_by="desc(Account.date_created)",
        foreign_keys="Account.user_id",
    )

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def set_email_confirm_token(self, email):
        self.email_confirm_token = token.encode(
            email,
            current_app.config["EMAIL_TOKEN_SECRET_KEY"],
            expiration_seconds=(60*60*2)
        )

    def set_forgot_password_token(self, uuid):
        self.email_confirm_token = token.encode(
            uuid,
            current_app.config["EMAIL_TOKEN_SECRET_KEY"],
            expiration_seconds=(60*60)
        )

    def set_auth_token(self, uuid):
        access_token = create_access_token(identity=self.uuid)
        self.auth_token = access_token

    @staticmethod
    def verify_auth_token(auth_token):
        try:
            uuid = get_jwt_identity()
        except (RuntimeError, KeyError):
            uuid = None

        if uuid is not None:
            user = User.query.filter_by(uuid=uuid).one_or_none()
            return user
        else:
            return None


class Account(db.Model):
    uuid = db.Column(db.String(40), primary_key=True, default=uuid.uuid1())
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    bio_data = db.Column(db.String, nullable=False)
    display_photo = db.Column(db.String, nullable=False, default="default-avatar.png")

    date_created = db.Column(db.DateTime, default=dt.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=dt.datetime.utcnow)

    user_id = db.Column(db.String(36), db.ForeignKey("user.uuid"))

    def __repr__(self):
        return '<Account %r>' % self.name


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
