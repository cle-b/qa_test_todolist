# -*- coding: utf-8 -


class Tag(object):
    def __init__(self, name=None):
        self.name = name
        self.url = None

    def __repr__(self):
        return f"{self.name} - {self.url}"

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name and self.url == other.url

    def __hash__(self):
        return hash((self.name, self.url))

    def to_json(self):
        return {"name": self.name}

    def from_json(self, json):
        self.name = json["name"]
        self.url = json["url"]
        return self
