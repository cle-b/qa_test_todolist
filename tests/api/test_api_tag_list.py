# -*- coding: utf-8 -*-
import pytest


@pytest.mark.api
@pytest.mark.tag
@pytest.mark.vcr()
def test_api_tag_list_anonymous(api, new_task_done_three_tags):
    """
    1. List all tags. The tags of a newly created tag is present.
    """
    tags = api.list_tags()
    for tag in new_task_done_three_tags.tags:
        assert tag in tags


@pytest.mark.api
@pytest.mark.tag
@pytest.mark.vcr()
def test_api_tag_list_with_user(api, new_user, new_task_done_three_tags):
    """
    1. Sign in.
    1. List all tags. The tags of a newly created tag is present.
    """
    api.authenticate(new_user.username, new_user.password)
    tags = api.list_tags()
    for tag in new_task_done_three_tags.tags:
        assert tag in tags
