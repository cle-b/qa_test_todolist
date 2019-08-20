# -*- coding: utf-8 -*-
import pytest

from todoapp.api import User, TodoAppApiException


@pytest.mark.api
@pytest.mark.user
@pytest.mark.vcr()
def test_api_user_create_user_success(api):
    """
    1. Create a user with a unique name and a unique password.
    """
    username = "test_api_user_create_user_success"
    password = "test_api_user_create_user_success"
    user = api.create_user(User(username, password))
    assert user.username == username


@pytest.mark.api
@pytest.mark.user
@pytest.mark.vcr()
@pytest.mark.parametrize(
    "username,password", [("", "onlypassword"), ("onlyusername", ""), ("", "")]
)
def test_api_user_create_user_with_uncomplete_informations(api, username, password):
    """
    1. Create a user with uncomplete informations (shall fail).
    """
    # TODO ask developers to handle correctly this case
    with pytest.raises(TodoAppApiException) as e_info:
        api.create_user(User(username, password))
    assert "HTTP 500" in str(e_info.value)


@pytest.mark.api
@pytest.mark.user
@pytest.mark.vcr()
def test_api_user_create_users_with_the_same_username(api):
    """
    1. Create a user with a unique name and a unique password.
    2. Create another user with the same informations (shall fail).
    """
    # TODO ask developers to handle correctly this case
    username = "test_api_user_create_the_same_user_twice"
    password = "test_api_user_create_the_same_user_twice"
    user = api.create_user(User(username, password))
    assert user.username == username
    with pytest.raises(TodoAppApiException) as e_info:
        api.create_user(User(username, password))
    assert "HTTP 500" in str(e_info.value)


@pytest.mark.api
@pytest.mark.user
@pytest.mark.bug
@pytest.mark.vcr()
def test_api_user_create_users_with_the_same_password(api):
    """
    1. Create a user with a unique name and a unique password.
    2. Create another user with another unique name but with the same password.
    """
    username1 = "test_api_user_create_users_with_the_same_password_1"
    username2 = "test_api_user_create_users_with_the_same_password_2"
    password = "test_api_user_create_users_with_the_same_password"
    user = api.create_user(User(username1, password))
    assert user.username == username1
    user = api.create_user(User(username2, password))
    assert user.username == username2


@pytest.mark.api
@pytest.mark.user
@pytest.mark.vcr()
def test_api_user_new_user_can_sign_in(api):
    """
    1. Create a user with a unique name and a unique password.
    2. Sign in with the new user.
    """
    username = "test_api_user_new_user_can_sign_in"
    password = "test_api_user_new_user_can_sign_in"
    user = api.create_user(User(username, password))
    assert user.username == username
    token = api.authenticate(username, password)
    assert token.username == username
