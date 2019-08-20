# -*- coding: utf-8 -*-
import pytest

from todoapp.api import Task, TodoAppApiException


@pytest.mark.api
@pytest.mark.authentication
@pytest.mark.vcr()
def test_api_authentication_success_basic(api, default_user, unique_task_title):
    """
    1. Sign in with the default user's credentials (using basic mode).
    2. Create a task.
    """
    # TODO ask developers to add a /me endpoint in order to make the authentication
    # tests cleaner when using the basic mode - instead we have to create task in order
    # to check if we are authenticated
    api.authenticate(default_user.username, default_user.password, mode="basic")
    api.create_task(Task(unique_task_title))


@pytest.mark.api
@pytest.mark.authentication
@pytest.mark.vcr()
def test_api_authentication_success_token(api, default_user):
    """
    1. Sign in with the default user's credentials (using token mode).
    """
    token = api.authenticate(default_user.username, default_user.password, mode="token")
    assert token.username == default_user.username


@pytest.mark.api
@pytest.mark.authentication
@pytest.mark.vcr()
@pytest.mark.parametrize(
    "username,password", [("nobody", "personne"), ("", "willWin"), ("QA", ""), ("", "")]
)
def test_api_authentication_failed_basic(api, username, password, unique_task_title):
    """
    1.  Sign in with bad credentials using basic mode
    2. Create a task (shall fail).
    """
    api.authenticate(username, password, mode="basic")
    with pytest.raises(TodoAppApiException) as e_info:
        api.create_task(Task(unique_task_title))
    assert "HTTP 401" in str(e_info.value)


@pytest.mark.api
@pytest.mark.authentication
@pytest.mark.vcr()
@pytest.mark.parametrize(
    "username,password", [("nobody", "personne"), ("", "willWin"), ("QA", ""), ("", "")]
)
def test_api_authentication_failed_token(api, username, password):
    """
    1.  Sign in with bad credentials using token mode (shall fail).
    """
    with pytest.raises(TodoAppApiException) as e_info:
        api.authenticate(username, password, mode="token")
    assert "HTTP 401" in str(e_info.value)
