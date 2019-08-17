# -*- coding: utf-8 -


class User(object):
    def __init__(self, username=None, password=None):
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
