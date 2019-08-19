# -*- coding: utf-8 -*-
import pytest

from todoapp.api import TodoAppApiException


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.vcr()
def test_api_task_update_task(api, new_user, new_task):
    """
    1. Sign in.
    2. Update a task owned by the authenticated user.
    3. Get task description. The task is updated.
    """
    api.authenticate(new_user.username, new_user.password)
    assert new_task.done is False
    assert new_task == api.get_task(new_task.id)
    new_task.done = True
    task_updated = api.update_task(new_task.id, new_task)
    assert task_updated == new_task
    assert api.get_task(new_task.id).done is True


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.vcr()
def test_api_task_update_task_anonymous(api, new_task):
    """
    1. As an anonymous user, update a task (shall failed).
    """
    assert new_task.done is False
    assert new_task == api.get_task(new_task.id)
    new_task.done = True
    with pytest.raises(TodoAppApiException) as e_info:
        api.update_task(new_task.id, new_task)
    assert "HTTP 401" in str(e_info.value)


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.vcr()
def test_api_task_update_task_another_user(api, new_task, default_user):
    """
    1. Sign in.
    2. Update a task owned by the another user (shall failed).
    """
    api.authenticate(default_user.username, default_user.password)
    assert new_task.done is False
    assert new_task == api.get_task(new_task.id)
    new_task.done = True
    with pytest.raises(TodoAppApiException) as e_info:
        api.update_task(new_task.id, new_task)
    assert "HTTP 403" in str(e_info.value)
