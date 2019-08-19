# -*- coding: utf-8 -*-
import pytest


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskget
@pytest.mark.vcr()
def test_api_task_get_task(api, new_user, new_task):
    """
    1. Sign in.
    2. Get description for a task owned by to the authenticated user.
    """
    api.authenticate(new_user.username, new_user.password)
    task = api.get_task(new_task.id)
    assert new_task == task


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskget
@pytest.mark.vcr()
def test_api_task_get_task_anonymous_user(api, new_task):
    """
    2. As an anonymous user, get description for a task owned by another user.
    """
    task = api.get_task(new_task.id)
    assert new_task == task
