import string
import random
import uuid

from api.models import User


def generate_number(length):
    return "".join(random.choice(string.digits) for _ in range(length))


def generate_username():
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))


def create_user(role, username=generate_username()):

    user_exist = User.query.filter_by(username=username).one_or_none()

    if user_exist:
        return user_exist

    user = User(
        uuid=uuid.uuid1(),
        username=username,
        email=username + "@mail.com",
        phone_number="072" + generate_number(7)
    )

    role.users.append(user)

    user.password = "password"
    user.set_password(user.password)
    user.set_email_confirm_token(user.email)

    return user
