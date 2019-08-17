# -*- coding: utf-8 -*-
import pytest


@pytest.mark.api
@pytest.mark.task
@pytest.mark.vcr()
def test_task_list_as_anonymous_user(api, new_task):
    """
    1. Check if an anonymous user could find a newly created task in the list
    of all tasks.
    """
    tasks = api.list_tasks()
    assert new_task in tasks


@pytest.mark.api
@pytest.mark.task
@pytest.mark.vcr()
def test_task_list_as_authentified_user(api, new_task, default_user):
    """
    1. Check if an authentified user could find a newly created task in the list
    of all tasks.
    """
    api.authenticate(default_user.username, default_user.password)
    tasks = api.list_tasks()
    assert new_task in tasks
