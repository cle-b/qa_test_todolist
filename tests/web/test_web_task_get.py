# -*- coding: utf-8 -*-
import pytest


@pytest.mark.web
@pytest.mark.task
def test_web_task_check_information(
    webapp, new_user, new_task, new_task_done, new_task_no_tag
):
    """
    1. Navigate to the HomePage.
    2. Check task details for a newly created task
    """
    webapp.homepage()
    for existing_task in (new_task, new_task_done, new_task_no_tag):
        task = webapp.taskboard.find_task(existing_task.title)
        assert task.title == existing_task.title
        assert task.done == existing_task.done
        assert task.owner == existing_task.username
        assert set(task.tags) == set([tag.name for tag in existing_task.tags])
        assert task.date == existing_task.date
