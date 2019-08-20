# -*- coding: utf-8 -*-
import pytest

from todoapp.api import TodoAppApiException


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.vcr()
def test_api_task_update_status(api, new_user, new_task):
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
    1. As an anonymous user, update a task (shall fail).
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
    2. Update a task owned by the another user (shall fail).
    """
    api.authenticate(default_user.username, default_user.password)
    assert new_task.done is False
    assert new_task == api.get_task(new_task.id)
    new_task.done = True
    with pytest.raises(TodoAppApiException) as e_info:
        api.update_task(new_task.id, new_task)
    assert "HTTP 403" in str(e_info.value)


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.vcr()
def test_api_task_update_title(api, new_user, new_task, unique_task_title):
    """
    1. Sign in.
    2. Update the title of a task owned by the authenticated user.
    3. Get task description. The task is updated.
    """
    api.authenticate(new_user.username, new_user.password)
    assert new_task.title != unique_task_title
    assert new_task == api.get_task(new_task.id)
    new_task.title = unique_task_title
    task_updated = api.update_task(new_task.id, new_task)
    assert task_updated == new_task
    assert api.get_task(new_task.id).title == unique_task_title


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.bug
@pytest.mark.vcr()
def test_api_task_update_title_too_long(
    api, new_user, new_task, unique_task_title_too_long
):
    """
    1. Sign in.
    2. Update the title of a task owned by the authenticated user. The new title
       length is 21 characters. (shall failed)
    """
    api.authenticate(new_user.username, new_user.password)
    new_task.title = unique_task_title_too_long
    with pytest.raises(TodoAppApiException):
        api.update_task(new_task.id, new_task)


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.tag
@pytest.mark.vcr()
def test_api_task_update_tag(api, new_user, new_task, unique_tag_name):
    """
    1. Sign in.
    2. Update the tag name of a task owned by the authenticated user.
    3. Get task description. The task is updated.
    """
    api.authenticate(new_user.username, new_user.password)
    assert new_task.tags[0].name != unique_tag_name
    assert new_task == api.get_task(new_task.id)
    new_task.tags[0].name = unique_tag_name
    task_updated = api.update_task(new_task.id, new_task)
    assert task_updated.tags[0].name == unique_tag_name
    assert api.get_task(new_task.id).tags[0].name == unique_tag_name


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.tag
@pytest.mark.vcr()
def test_api_task_update_tag_too_long(
    api, new_user, new_task, unique_tag_name_too_long
):
    """
    1. Sign in.
    2. Update the tag name of a task owned by the authenticated user.
       The new tag name length is 21 characters. (shall failed)
    """
    api.authenticate(new_user.username, new_user.password)
    assert new_task.tags[0].name != unique_tag_name_too_long
    assert new_task == api.get_task(new_task.id)
    new_task.tags[0].name = unique_tag_name_too_long
    with pytest.raises(TodoAppApiException):
        api.update_task(new_task.id, new_task)
