# -*- coding: utf-8 -*-
import pytest


@pytest.mark.web
@pytest.mark.task
@pytest.mark.abc
def test_web_task_anonymous_cant_change_status(webapp, new_task, new_task_done):
    """
    1. Navigate to the HomePage.
    2. Verify that 'mark done' and 'mark in progress' options are unavailable
    for all tasks for an anonymous user.
    """
    webapp.homepage()
    for task in webapp.taskboard.tasks():
        assert "mark_done" not in task.options
        assert "mark_in_progress" not in task.options


@pytest.mark.web
@pytest.mark.task
@pytest.mark.abc
def test_web_task_change_status_option_only_for_own_tasks(
    webapp, new_user, new_task, new_task_default_user
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. Verify that 'mark done' and 'mark in progress' options are available
    only for tasks owned by this user.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    for task in webapp.taskboard.tasks():
        assert (
            ("mark_done" in task.options) or ("mark_in_progress" in task.options)
        ) == (task.owner == new_user.username)


@pytest.mark.web
@pytest.mark.task
@pytest.mark.abc
def test_web_task_update_status_to_done(webapp, new_user, new_task):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present, the task is in progress.
    4. Update the status to done.
    5. The task status is done.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task.title)
    assert task.done is False
    task.mark_done()
    assert task.done is True


@pytest.mark.web
@pytest.mark.task
@pytest.mark.abc
def test_web_task_update_status_to_in_progress(webapp, new_user, new_task_done):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present, the task is done.
    4. Update the status to in progress.
    5. The task status is in progress.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task_done.title)
    assert task.done is True
    task.mark_in_progress()
    assert task.done is False
