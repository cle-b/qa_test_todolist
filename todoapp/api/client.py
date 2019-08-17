# -*- coding: utf-8 -
import requests

from .user import User
from .task import Task
from .tag import Tag
from .token import Token


class TodoAppApiException(Exception):
    def __init__(self, message, status_code, content):
        self.message = message
        self.status_code = status_code
        self.content = content

    def __repr__(self):
        return f"{self.message}: (HTTP {self.status_code}) - {self.content}"

    def __str__(self):
        return f"{self.message}: (HTTP {self.status_code}) - {self.content}"


def check_status(response, expected_status, error_message):
    if not response.status_code == expected_status:
        raise TodoAppApiException(error_message, response.status_code, response.text)


class TodoAppAPI(object):
    def __init__(self, base_url):
        self.base_url = base_url  # TODO remove last /
        self.session = requests.Session()

    def _auth_basic(self, username, password):
        self.session.auth = (username, password)

    def _auth_token(self, username, password):
        payload = {"username": username, "password": password}
        response = self.session.post(f"{self.base_url}/authenticate", json=payload)

        check_status(response, 200, "Authentication failed")

        token = Token().from_json(response.json())

        self.session.auth = (token.token, "dataiku")

        return token

    def authenticate(self, username, password, mode="token"):
        if mode == "basic":
            return self._auth_basic(username, password)
        elif mode == "token":
            return self._auth_token(username, password)
        else:
            raise ValueError(f"mode value shall be basic or token, not {mode}")

    def reset(self):
        response = self.session.get(f"{self.base_url}/reset")

        check_status(response, 200, "Unable to reset app")

    def create_user(self, user):
        response = self.session.post(f"{self.base_url}/users", json=user.to_json())

        check_status(response, 200, "Unable to reset user")

        return User().from_json(response.json())

    def list_tasks(self):
        response = self.session.get(f"{self.base_url}/")

        check_status(response, 200, "Unable to retrieve tasks")

        return [Task().from_json(task) for task in response.json()]

    def create_task(self, task):
        response = self.session.put(f"{self.base_url}/", json=task.to_json())

        check_status(response, 200, "Unable to create task")

        return Task().from_json(response.json())

    def get_task(self, id):
        response = self.session.get(f"{self.base_url}/{id}")

        check_status(response, 200, f"Unable to retrieve task {id}")

        return Task().from_json(response.json())

    def delete_task(self, id):
        response = self.session.delete(f"{self.base_url}/{id}")

        check_status(response, 200, f"Unable to delete task {id}")

        return True

    def update_task(self, id, task):
        response = self.session.patch(f"{self.base_url}/{id}", json=task.to_json())

        check_status(response, 200, f"Unable to update task {id}")

        return Task().from_json(response.json())

    def list_tags(self):
        response = self.session.get(f"{self.base_url}/tags")

        check_status(response, 200, "Unable to list tags")

        return [Tag().from_json(tag) for tag in response.json()]

    def get_tag(self, id):
        response = self.session.get(f"{self.base_url}/tags/{id}")

        check_status(response, 200, f"Unable to retrieve tag {id}")

        return Tag().from_json(response.json())
