# -*- coding: utf-8 -
from .tag import Tag
from .user import User


class Task(object):
    def __init__(self, title=None, tags=[]):
        self.title = title
        self.tags = tags
        self.date = None
        self.done = None
        self.id = None
        self.username = None

    def __repr__(self):
        return f"{self.id} - {self.title} - {self.done}"

    def __str__(self):
        return f"{self.title}"

    def to_json(self):
        return {
            "title": self.title,
            "tags": [tag.name for tag in self.tags],
            "date": self.date,
            "done": self.done,
            "id": self.id,
            "username": self.username,
        }

    def from_json(self, json):
        self.title = json["title"]
        self.tags = [Tag().from_json(title) for title in json["tags"]]
        self.date = json["date"]
        self.done = json["done"]
        self.id = json["id"]
        self.username = User(json["username"])
        return self
