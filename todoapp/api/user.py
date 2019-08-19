# -*- coding: utf-8 -


class User(object):
    """A user

    Params:
        username {str} -- the username
        password {str} -- the password
    """

    def __init__(self, username=None, password=None):
        """User description

        Arguments:
            username {str} -- the username (default: {None})
            password {str} -- the password (default: {None})
        """
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username} - {self.password}"

    def __str__(self):
        return f"{self.username}"

    def to_json(self):
        return {"username": self.username, "password": self.password}

    def from_json(self, json):
        self.username = json["username"]
        return self
