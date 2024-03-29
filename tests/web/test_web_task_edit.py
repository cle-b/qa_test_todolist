# -*- coding: utf-8 -*-
import pytest


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_anonymous_cant_edit(webapp, new_task):
    """
    1. Navigate to the HomePage.
    2. Verify that edit option is unavailable for all tasks for an anonymous user.
    """
    webapp.homepage()
    for task in webapp.taskboard.tasks():
        assert "edit" not in task.options


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_edit_option_only_for_own_tasks(
    webapp, new_user, new_task, new_task_default_user
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. Verify that edit option is available only for tasks owned by this user.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    for task in webapp.taskboard.tasks():
        assert ("edit" in task.options) == (task.owner == new_user.username)


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_edit_title(webapp, new_user, new_task, unique_task_title):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present.
    4. Update the title of a task owned by the authenticated user.
    5. List the tasks. The title of the task is updated ().
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task.title)
    task.edit(title=unique_task_title)
    assert task.title == unique_task_title


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_edit_status_to_done(webapp, new_user, new_task):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present, the task is in progress.
    4. Edit the task and set the status to done.
    5. The task status is done.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task.title)
    assert task.done is False
    task.edit(done=True)
    assert task.done is True


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_edit_status_to_in_progress(
    webapp, new_user, new_task_done_three_tags
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present, the task is done.
    4. Edit the task and set the status to in progress.
    5. The task status is in progress.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task_done_three_tags.title)
    assert task.done is True
    task.edit(done=False)
    assert task.done is False


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_edit_title_with_already_existing_title(
    webapp, new_user, new_task, new_task_no_tag
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present.
    4. Update the title of a task owned by the authenticated user
       with the title of another task. (shall fail).
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task.title)
    with pytest.raises(AssertionError):
        task.edit(title=new_task_no_tag.title)


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.bug
def test_web_task_edit_title_with_too_long_title(
    webapp, new_user, new_task, new_task_no_tag, unique_task_title_too_long
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present.
    4. Update the title of a task owned by the authenticated user
       with the title too long (21 characters) (shall fail).
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task.title)
    with pytest.raises(AssertionError):
        task.edit(title=unique_task_title_too_long)


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
@pytest.mark.bug
def test_web_task_edit_change_tag_name(
    webapp, new_user, new_task_done_three_tags, unique_tag_name
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present.
    4. Update a tag name of a task owned by the authenticated user.
    5. Navigate to the HomePage (refresh the taskboard).
    6. List the tasks. The newly created task is present.
    7. The tag name is still updated.
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task_done_three_tags.title)
    old_tag_name = new_task_done_three_tags.tags[0].name
    new_tag_name = unique_tag_name
    task.edit(tags={old_tag_name: new_tag_name})
    webapp.homepage()
    task = webapp.taskboard.find_task(new_task_done_three_tags.title)
    assert old_tag_name not in task.tags
    assert new_tag_name in task.tags


@pytest.mark.web
@pytest.mark.task
@pytest.mark.taskupdate
def test_web_task_edit_change_tag_name_too_long_name(
    webapp, new_user, new_task_done_three_tags, unique_tag_name_too_long
):
    """
    1. Navigate to the HomePage.
    2. Sign in.
    3. List the tasks. The newly created task is present.
    4. Update a tag name of a task owned by the authenticated user
       with a name too long (21 characters) (shall fail)
    """
    webapp.homepage()
    webapp.sign_in(new_user.username, new_user.password)
    task = webapp.taskboard.find_task(new_task_done_three_tags.title)
    old_tag_name = new_task_done_three_tags.tags[0].name
    new_tag_name = unique_tag_name_too_long
    with pytest.raises(AssertionError):
        task.edit(tags={old_tag_name: new_tag_name})
