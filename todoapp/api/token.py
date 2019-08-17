# -*- coding: utf-8 -


class Token(object):
    def __init__(self):
        self.username = None
        self.token = None
        self.expires = None

    def __repr__(self):
        return f"{self.username} - {self.expires} - {self.token}"

    def __str__(self):
        return f"{self.username} - {self.expires} - {self.token}"

    def from_json(self, json):
        self.username = json["username"]
        self.token = json["token"]
        self.expires = json["expires"]
        return self
