# -*- coding: utf-8 -*-
import pytest
from selenium.common.exceptions import WebDriverException


@pytest.mark.web
@pytest.mark.authentication
def test_web_authentication_success(webapp, default_user):
    """
    1. Navigate to the Homepage.
    2. Sign in with right credentials.
    """
    webapp.homepage()
    webapp.sign_in(default_user.username, default_user.password)
    assert webapp.me == default_user.username


@pytest.mark.web
@pytest.mark.authentication
@pytest.mark.parametrize(
    "username,password", [("nobody", "personne"), ("", "willWin"), ("QA", ""), ("", "")]
)
def test_web_authentication_fail(webapp, username, password):
    """
    1. Navigate to the Homepage.
    2. Sign in with wrong credentials (shall failed).
    """
    webapp.homepage()
    with pytest.raises(WebDriverException):
        webapp.sign_in(username, password)
