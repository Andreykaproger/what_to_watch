import pytest

from opinions_app import create_app, db
from opinions_app.models import User, Opinion, OpinionStatus, UserRole

from settings import TestConfig

@pytest.fixture
def app():

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture
def user(app):

    user = User(
        username = "testuser_pro",
        email = "test@test.com"
    )
    user.set_password("password")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin(app):

    user = User(
        username = "admin",
        email = "admin@admin.com",
        role = UserRole.ADMIN
    )
    user.set_password("password")

    db.session.add(user)
    db.session.commit()

    return user

@pytest.fixture
def auth_web(client, user):

    return client.post(
        "/login",
        data={
            "email": user.email,
            "password": "password"
        }
    )


@pytest.fixture
def admin_auth_tokens(client, admin):

    response = client.post(
        "/api/auth/login",
        json={
            "email": admin.email,
            "password": "password"
        }
    )

    return response.json

@pytest.fixture
def auth_tokens(client, user):

    response = client.post(
        "/api/auth/login",
        json={
            "email": user.email,
            "password": "password"
        }
    )

    return response.json

@pytest.fixture
def opinion(app, user):

    opinion = Opinion(
        title = "Opinion",
        text = "Opinion text",
        user_id = user.id,
        status = OpinionStatus.APPROVED
    )

    db.session.add(opinion)
    db.session.commit()

    return opinion

@pytest.fixture
def pending_opinion(app, user):

    opinion = Opinion(
        title = "Pending Opinion",
        text = "Pending Opinion text",
        user_id = user.id,
        status = OpinionStatus.PENDING
    )

    db.session.add(opinion)
    db.session.commit()

    return opinion

@pytest.fixture
def blocked_user(app):

    user = User(
        username = "blocked_user",
        email = "blocked@test.com",
        is_active = False,
        block_reason = "Нарушение правил"
    )
    user.set_password("password")

    db.session.add(user)
    db.session.commit()

    return user