# -*- coding: utf-8 -*-
import pytest


@pytest.mark.web
@pytest.mark.task
def test_web_task_anonymous_cant_delete(webapp, new_task):
    """
    1. Navigate to the HomePage.
    2. Verify that delete option is unavailable for all tasks
    for an anonymous user.
    """
    webapp.homepage()
    for task in webapp.taskboard.tasks():
        assert "delete" not in task.options


@pytest.mark.web
@pytest.mark.task
def test_web_task_delete_option_only_for_own_tasks(
    webapp, new_user, new_task, new_task_default_user
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. Verify that delete option is available only for tasks owned by this user.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    for task in webapp.taskboard.tasks():
        assert ("delete" in task.options) == (task.owner == new_user.username)


@pytest.mark.web
@pytest.mark.task
def test_web_task_delete_task(webapp, new_user, new_task):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present.
    4. Delete a task owned by to the authenticated user.
    5. List the tasks. The deleted task is not present.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task.title)
    task.delete()
    assert new_task.title not in [task.title for task in webapp.taskboard.tasks()]
