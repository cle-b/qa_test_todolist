# -*- coding: utf-8 -*-
import pytest


@pytest.mark.web
@pytest.mark.task
def test_web_task_list_as_anonymous_user(webapp, new_task):
    """
    1. Navigate to the HomePage.
    2. Check if an anonymous user could find a newly created task in the list
    of all tasks.
    """
    webapp.homepage()
    webapp.taskboard.find_task(new_task.title)


@pytest.mark.web
@pytest.mark.task
def test_web_task_list_as_authentified_user(webapp, new_task, default_user):
    """
    1. Navigate to the HomePage.
    2. Check if an authentified user could find a newly created task in the list
    of all tasks.
    """
    webapp.homepage()
    webapp.sign_in(default_user.username, default_user.password)
    webapp.taskboard.find_task(new_task.title)
