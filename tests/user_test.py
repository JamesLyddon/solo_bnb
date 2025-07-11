import pytest
from lib.user import User

@pytest.fixture
def user():
    return User(1, 'johndoe', 'john.doe@example.com', 'hashedpassword123', 'John', 'Doe')

def test_user_constructs(user):
    assert isinstance(user, User)

def test_user_formats_nicely(user):
    assert str(user) == "User(1, johndoe, john.doe@example.com, John, Doe)"

def test_artists_are_equal():
    user_1 = User(1, 'johndoe', 'john.doe@example.com', 'hashedpassword123', 'John', 'Doe')
    user_2 = User(1, 'johndoe', 'john.doe@example.com', 'hashedpassword123', 'John', 'Doe')
    assert user_1 == user_2
