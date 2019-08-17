# -*- coding: utf-8 -
import os
import sys
import shutil

import pytest

from todoapp.api import TodoAppAPI


for env in ["QA_TODOAPP_BASEURL", "QA_TODOAPP_USERNAME", "QA_TODOAPP_PASSWORD"]:
    if env not in os.environ:
        print(f"{env} environment variable is missing - please check your environment")
        sys.exit(-1)


@pytest.fixture(scope="session")
def base_url():
    return os.environ["QA_TODOAPP_BASEURL"]


@pytest.fixture(scope="session")
def default_user():
    return {
        "username": os.environ["QA_TODOAPP_USERNAME"],
        "password": os.environ["QA_TODOAPP_PASSWORD"],
    }


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
