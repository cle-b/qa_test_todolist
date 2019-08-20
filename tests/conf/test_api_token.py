# -*- coding: utf-8 -*-
import time

import pytest

from todoapp.api import Task, TodoAppApiException


@pytest.mark.conf
@pytest.mark.conftoken
@pytest.mark.vcr()
def test_api_conf_token_expiration(api, default_user, unique_task_title):
    """
    1. Authenticate with the default user's credentials (using token mode).
    2. Wait 30 seconds and create a task (x19)
    3. Wait for 30 seconds.
    3. Create a task. (shall fail)
    """
    token = api.authenticate(default_user.username, default_user.password, mode="token")
    assert token.username == default_user.username
    for i in range(19):
        time.sleep(30)
        api.create_task(Task(f"{unique_task_title}{i}"))
    time.sleep(30)
    with pytest.raises(TodoAppApiException) as e_info:
        api.create_task(Task(f"{unique_task_title}{i+1}"))
    assert "HTTP 401" in str(e_info.value)
