import pytest


from app import db

from app.users.models import User


@pytest.fixture(scope='module')
def setup():
    # setup
    session = db.get_session()
    yield session
    # tear down
    q = User.objects.filter(email='test@test.com')
    if q.count() != 0:
        q.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email='test@test.com', password='password')


def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='password')


def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@t', password='password')


def test_valid_password(setup):
    q = User.objects.filter(email='test@test.com')
    assert q.count() == 1
    user = q.first()
    assert user.verify_password('password') == True
    assert user.verify_password('password123') == False
