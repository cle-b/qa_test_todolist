# -*- coding: utf-8 -
from urllib.parse import urljoin

import requests

from .user import User
from .task import Task
from .tag import Tag
from .token import Token


class TodoAppApiException(Exception):
    """Default Exception for the REST API client
    """

    def __init__(self, message, status_code, content):
        """An exception occurs in the REST API client.

        Arguments:
            message {str} -- the reason of the exception
            status_code {int} -- HTTP status code
            content {type} -- the response body
        """
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
    """A REST API client for the TodoApp.
    """

    def __init__(self, base_url):
        """Initialize the client.

        Arguments:
            base_url {str} -- the landing page URL
        """
        self.base_url = urljoin(base_url, "/")[:-1]  # remove the last /
        self.session = requests.Session()

    def __repr__(self):
        return f"base_url {self.base_url}"

    def __str__(self):
        return f"base_url {self.base_url}"

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
        """User authentication

        Arguments:
            username {str} -- the username
            password {str} -- the password

        Keyword Arguments:
            mode {str} -- the authorization method (basic|token) (default: {"token"})

        Raises:
            ValueError: the authorization method is unknown
            TodoAppApiException: unable to get the token

        Returns:
            str -- the token (or None if the authorization method is basic)
        """
        if mode == "basic":
            return self._auth_basic(username, password)
        elif mode == "token":
            return self._auth_token(username, password)
        else:
            raise ValueError(f"mode value shall be basic or token, not {mode}")

    def reset(self):
        """Reset the database

        Raises:
            TodoAppApiException: unable to reset the database
        """
        response = self.session.get(f"{self.base_url}/reset")

        check_status(response, 200, "Unable to reset app")

    def create_user(self, user):
        """Create a new user

        Arguments:
            user {User} -- the user description

        Returns:
            User -- the new user

        Raises:
            TodoAppApiException: unable to create a new user
        """
        response = self.session.post(f"{self.base_url}/users", json=user.to_json())

        check_status(response, 200, "Unable to create user")

        return User().from_json(response.json())

    def list_tasks(self):
        """List all available tasks.

        Returns:
            [Task] -- A list of tasks

        Raises:
            TodoAppApiException: unable to retrieve tasks
        """
        response = self.session.get(f"{self.base_url}/")

        check_status(response, 200, "Unable to retrieve tasks")

        return [Task().from_json(task) for task in response.json()]

    def create_task(self, task):
        """Create a new task

        Arguments:
            task {Task} -- the task description

        Returns:
            Task -- the new task

        Raises:
            TodoAppApiException: unable to create a new task
        """
        response = self.session.put(f"{self.base_url}/", json=task.to_json())

        check_status(response, 200, "Unable to create task")

        return Task().from_json(response.json())

    def get_task(self, id):
        """Get task by id

        Arguments:
            id {int} -- the task id

        Returns:
            Task -- the expected task

        Raises:
            TodoAppApiException: unable to retrieve the task
        """
        response = self.session.get(f"{self.base_url}/{id}")

        check_status(response, 200, f"Unable to retrieve task {id}")

        return Task().from_json(response.json())

    def delete_task(self, id):
        """Delete a task

        Arguments:
            id {int} -- the id of the task to delete

        Returns:
            bool -- True

        Raises:
            TodoAppApiException: unable to delete the task
        """
        response = self.session.delete(f"{self.base_url}/{id}")

        check_status(response, 200, f"Unable to delete task {id}")

        return True

    def update_task(self, id, task):
        """Update a task

        Arguments:
            id {int} -- the id of the task to update
            task {Task} -- the new task description

        Returns:
            Task -- the updated task

        Raises:
            TodoAppApiException: unable to update the task
        """
        response = self.session.patch(f"{self.base_url}/{id}", json=task.to_json())

        check_status(response, 200, f"Unable to update task {id}")

        return Task().from_json(response.json())

    def list_tags(self):
        """List all the tags

        Returns:
            [Tag] -- A list of tags

        Raises:
            TodoAppApiException: unable to retrieve the list of tags
        """
        response = self.session.get(f"{self.base_url}/tags")

        check_status(response, 200, "Unable to list tags")

        return [Tag().from_json(tag) for tag in response.json()]

    def get_tag(self, id):
        """Get the tag description

        Arguments:
            id {int} -- the id of the tag

        Returns:
            Tag -- the tag description

        Raises:
            TodoAppApiException: unable to retrieve the tag description
        """
        response = self.session.get(f"{self.base_url}/tags/{id}")

        check_status(response, 200, f"Unable to retrieve tag {id}")

        return Tag().from_json(response.json())
