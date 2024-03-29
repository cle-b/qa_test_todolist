# -*- coding: utf-8 -*-
import pytest

from todoapp.api import Task, Tag, TodoAppApiException


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_task(api, new_user, unique_task_title):
    """
    1. Sign in.
    2. Create a task with no tag.
    """
    api.authenticate(new_user.username, new_user.password)
    task = api.create_task(Task(unique_task_title))
    assert task.title == unique_task_title
    assert len(task.tags) == 0


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_task_with_one_tag(
    api, new_user, unique_task_title, unique_tag_name
):
    """
    1. Sign in.
    2. Create a task with one tag.
    """
    api.authenticate(new_user.username, new_user.password)
    task = api.create_task(Task(unique_task_title, [Tag(unique_tag_name)]))
    assert task.title == unique_task_title
    assert task.tags[0].name == unique_tag_name


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_task_with_many_tags(
    api, new_user, unique_task_title, unique_tag_name
):
    """
    1. Sign in.
    2. Create a task with two tags.
    """
    api.authenticate(new_user.username, new_user.password)
    tag_names = [f"{unique_tag_name}1", f"{unique_tag_name}2"]
    task = api.create_task(Task(unique_task_title, [Tag(name) for name in tag_names]))
    assert task.title == unique_task_title
    assert set(tag_names) == set([tag.name for tag in task.tags])


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_task_anonymous(api, unique_task_title):
    """
    1. Create a task (user not authentified) (shall fail)
    """
    with pytest.raises(TodoAppApiException) as e_info:
        api.create_task(Task(unique_task_title))
    assert "HTTP 401" in str(e_info.value)


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_task_empty_title(api, new_user):
    """
    1. Sign in.
    2. Create a task with an empty title
    """
    api.authenticate(new_user.username, new_user.password)
    task = api.create_task(Task(""))
    assert task.title == ""


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_two_tasks_with_same_title(api, new_user, unique_task_title):
    """
    1. Sign in.
    2. Create a task with a unique title
    3. Create a task with the same title (shall fail)
    """
    api.authenticate(new_user.username, new_user.password)
    api.create_task(Task(unique_task_title))
    with pytest.raises(TodoAppApiException):
        api.create_task(Task(unique_task_title))


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_two_tasks_with_same_tag(
    api, new_user, unique_task_title, unique_tag_name
):
    """
    1. Sign in.
    2. Create a task with a unique title and a unique tag
    3. Create a task with another title and the same tag
    """
    api.authenticate(new_user.username, new_user.password)
    task1 = api.create_task(Task(f"{unique_task_title}1", [Tag(unique_tag_name)]))
    task2 = api.create_task(Task(f"{unique_task_title}2", [Tag(unique_tag_name)]))
    assert task1.tags[0].name == unique_tag_name
    assert task2.tags[0].name == unique_tag_name


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.vcr()
def test_api_task_create_task_with_a_long_title(api, new_user, unique_task_title):
    """
    1. Sign in.
    2. Create a task with a unique title with 20 characters.
    """
    api.authenticate(new_user.username, new_user.password)
    long_title = f"{unique_task_title}{'A'*20}"[:20]
    task = api.create_task(Task(long_title))
    assert task.title == long_title


@pytest.mark.api
@pytest.mark.task
@pytest.mark.taskcreate
@pytest.mark.bug
@pytest.mark.vcr()
def test_api_task_create_task_with_a_too_long_title(
    api, new_user, unique_task_title_too_long
):
    """
    1. Sign in.
    2. Create a task with a unique title with 21 characters (shall fail).
    """
    api.authenticate(new_user.username, new_user.password)
    with pytest.raises(TodoAppApiException):
        api.create_task(Task(unique_task_title_too_long))
