# -*- coding: utf-8 -
import os
import sys
import shutil
import string
import secrets

import pytest

from todoapp.api import TodoAppAPI, User, Task, Tag


for env in ["QA_TODOAPP_BASEURL", "QA_TODOAPP_USERNAME", "QA_TODOAPP_PASSWORD"]:
    if env not in os.environ:
        print(f"{env} environment variable is missing - please check your environment")
        sys.exit(-1)


@pytest.fixture(scope="session")
def base_url():
    return os.environ["QA_TODOAPP_BASEURL"]


@pytest.fixture(scope="session")
def default_user():
    return User(os.environ["QA_TODOAPP_USERNAME"], os.environ["QA_TODOAPP_PASSWORD"])


@pytest.fixture(scope="session", autouse=True)
def reset(base_url):
    api = TodoAppAPI(base_url)
    api.reset()


@pytest.fixture
def api(base_url):
    return TodoAppAPI(base_url)


cassette_library_dir = "cassettes"

shutil.rmtree(cassette_library_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "cassette_library_dir": cassette_library_dir,
        "record_mode": "all",
        "decode_compressed_response": True,
    }


def random_name(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(16))


@pytest.fixture
def unique_task_title():
    return random_name(16)


@pytest.fixture
def unique_tag_name():
    return random_name(16)


@pytest.fixture
def new_user(base_url):
    api = TodoAppAPI(base_url)
    user = User(random_name(16), random_name(16))
    api.create_user(user)
    return user


@pytest.fixture
def new_task(base_url, new_user):
    api = TodoAppAPI(base_url)
    api.authenticate(new_user.username, new_user.password)
    task = api.create_task(Task(random_name(16), [Tag(random_name(16))]))
    return task
