# -*- coding: utf-8 -
import os
import sys
import shutil
import string
import secrets
from urllib.parse import urljoin

import pytest
from py.xml import html

from todoapp.api import TodoAppAPI, User, Task, Tag
from todoapp.web import HomePage

import niobium  # noqa: F401 - niobium automatically patches selenium


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


CASSETTE_LIBRARY_DIR = "assets"

shutil.rmtree(CASSETTE_LIBRARY_DIR, ignore_errors=True)


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "cassette_library_dir": CASSETTE_LIBRARY_DIR,
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


@pytest.fixture
def new_task_done(base_url, new_user):
    api = TodoAppAPI(base_url)
    api.authenticate(new_user.username, new_user.password)
    task = api.create_task(Task(random_name(16), [Tag(random_name(16))]))
    task.done = True
    updated_task = api.update_task(task.id, task)
    return updated_task


@pytest.fixture
def new_task_no_tag(base_url, new_user):
    api = TodoAppAPI(base_url)
    api.authenticate(new_user.username, new_user.password)
    task = api.create_task(Task(random_name(16), []))
    return task


@pytest.fixture
def new_task_default_user(base_url, default_user):
    api = TodoAppAPI(base_url)
    api.authenticate(default_user.username, default_user.password)
    task = api.create_task(Task(random_name(16), [Tag(random_name(16))]))
    return task


@pytest.fixture
def webapp(selenium, base_url):
    selenium.implicitly_wait(5)
    return HomePage(urljoin(base_url, "/web/index.html"), selenium)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # add HTTP trace for the API tests only
        if report.location[2].startswith("test_api"):
            extra.append(
                pytest_html.extras.url(
                    f"{CASSETTE_LIBRARY_DIR}/{report.location[2]}.yaml", name="HTTP"
                )
            )
        report.extra = extra


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div(report.description, class_="empty log"))
