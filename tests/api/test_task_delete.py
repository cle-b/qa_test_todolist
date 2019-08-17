# -*- coding: utf-8 -*-
import pytest

from todoapp.api import TodoAppApiException


@pytest.mark.api
@pytest.mark.task
@pytest.mark.vcr()
def test_task_delete_task(api, new_user, new_task):
    """
    1. Sign in.
    2. List the tasks. The newly created task is present.
    3. Delete a task owned by to the authenticated user.
    4. List the tasks. The deleted task is not present.
    """
    api.authenticate(new_user.username, new_user.password)
    assert new_task in api.list_tasks()
    api.delete_task(new_task.id)
    assert new_task not in api.list_tasks()


@pytest.mark.api
@pytest.mark.task
@pytest.mark.vcr()
def test_task_delete_task_anonymous(api, new_task):
    """
    1. List the tasks. The newly created task is present.
    2. Delete a task owned by to the authenticated user (shall failed).
    """
    assert new_task in api.list_tasks()
    with pytest.raises(TodoAppApiException) as e_info:
        api.delete_task(new_task.id)
    assert "HTTP 401" in str(e_info.value)


@pytest.mark.api
@pytest.mark.task
@pytest.mark.vcr()
@pytest.mark.bug
def test_task_delete_task_another_user(api, new_task, default_user):
    """
    1. Sign in.
    2. List the tasks. The newly created task is present.
    3. Delete a task not owned by to the authenticated user (shall failed).
    """
    api.authenticate(default_user.username, default_user.password)
    assert new_task in api.list_tasks()
    assert new_task.username != default_user.username
    with pytest.raises(TodoAppApiException) as e_info:
        api.delete_task(new_task.id)
    assert "HTTP 401" in str(e_info.value)
