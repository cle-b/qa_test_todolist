# -*- coding: utf-8 -
from .tag import Tag


class Task(object):
    """A task

    Params:
        title {str} -- the task title (max 20 chars, shall be unique) (can be updated)
        tags {[Tag]} -- A list of tags (can be updated)
        date {str} -- the creation date
        done {str} -- the task status - (can be updated)
        id {int} -- the task id
        username {str} -- the task owner
    """

    def __init__(self, title=None, tags=[]):
        """Task description

        Keyword Arguments:
            title {str} -- the title task (default: {None})
            tags {[str]} -- A list of tag name (default: {[]})
        """
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

    def __eq__(self, other):
        return (
            self.title == other.title
            and set(self.tags) == set(other.tags)
            and self.date == other.date
            and self.done == other.done
            and self.id == other.id
            and self.username == other.username
        )

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
        self.tags = [Tag().from_json(tag) for tag in json["tags"]]
        self.date = json["date"]
        self.done = json["done"]
        self.id = json["id"]
        self.username = json["username"]
        return self
