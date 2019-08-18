# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from .base import BasePage


class TaskBoardPage(BasePage):

    __selectors = {
        "tasks": (By.CSS_SELECTOR, "tr:not(:first-of-type)"),
        "task_by_title": (
            By.XPATH,
            "//b[@data-bind='text: title' and contains(text(),'{title}')]/ancestor::tr",
        ),
    }

    def tasks(self):
        return [
            TaskPage(self.base_url, self.driver, task_elt)
            for task_elt in self.root.find_elements(*self.__selectors["tasks"])
        ]

    def find_task(self, title, timeout=None):
        return TaskPage(
            self.base_url,
            self.driver,
            self.root.find_element(
                self.__selectors["task_by_title"][0],
                self.__selectors["task_by_title"][1].format(title=title),
            ).wait(timeout=timeout),
        )


class TaskPage(BasePage):

    __selectors = {
        "title": (By.CSS_SELECTOR, "[data-bind='text: title']"),
        "done": (By.CSS_SELECTOR, "[data-bind='visible: done']"),
        "owner": (By.CSS_SELECTOR, "[data-bind='text: username']"),
        "tag": (By.CLASS_NAME, "task-tag"),
        "date": (By.CSS_SELECTOR, "[data-bind='text: date']"),
        "edit": (By.CSS_SELECTOR, "button[data-bind*='$parent.beginEdit']"),
        "delete": (By.CSS_SELECTOR, "button[data-bind*='$parent.remove']"),
        "mark_done": (By.CSS_SELECTOR, "button[data-bind*='$parent.markDone']"),
        "mark_in_progress": (
            By.CSS_SELECTOR,
            "button[data-bind*='$parent.markInProgress']",
        ),
        "edit_popup": (By.ID, "edit"),
        "edit_popup_title": (By.CSS_SELECTOR, "[data-bind='value: title']"),
        "edit_popup_done": (By.CSS_SELECTOR, "[data-bind='checked: done']"),
        "edit_popup_cancel": (By.CLASS_NAME, "close"),
        "edit_popup_save": (By.CSS_SELECTOR, "[data-bind='click:editTask']"),
    }

    @property
    def title(self):
        return self.root.find_element(*self.__selectors["title"]).text

    @property
    def done(self):
        return self.root.find_element(*self.__selectors["done"]).is_displayed()

    @property
    def owner(self):
        return self.root.find_element(*self.__selectors["owner"]).text

    @property
    def tags(self):
        return [
            tag_elt.text
            for tag_elt in self.root.find_elements(*self.__selectors["tag"])
        ]

    @property
    def date(self):
        return self.root.find_element(*self.__selectors["date"]).text

    @property
    def options(self):
        opts = []
        for opt in ["edit", "delete", "mark_done", "mark_in_progress"]:
            if self.root.find_element(*self.__selectors[opt]).is_displayed():
                opts.append(opt)
        return opts

    def edit(self, title=None, done=None):
        self.root.find_element(*self.__selectors["edit"]).wait().click()

        edit_popup_elt = self.driver.find_element(
            *self.__selectors["edit_popup"]
        ).wait()

        if title is not None:
            edit_popup_title = edit_popup_elt.find_element(
                *self.__selectors["edit_popup_title"]
            ).wait()
            edit_popup_title.clear()
            edit_popup_title.send_keys(title)

        if done is not None:
            edit_popup_done = edit_popup_elt.find_element(
                *self.__selectors["edit_popup_done"]
            ).wait()
            if edit_popup_done.is_selected() != done:
                edit_popup_done.click()

        if (title is not None) or (done is not None):
            close_button_elt = edit_popup_elt.find_element(
                *self.__selectors["edit_popup_save"]
            ).wait()
        else:
            close_button_elt = edit_popup_elt.find_element(
                *self.__selectors["edit_popup_cancel"]
            ).wait()

        close_button_elt.click()

        # just wait until the edit popup is closed
        self.root.find_element(*self.__selectors["title"]).wait()

        if title is not None:
            assert (
                self.root.find_element(*self.__selectors["title"]).wait().text == title
            )

        if done is not None:
            assert (
                self.root.find_element(*self.__selectors["done"]).is_displayed() == done
            )

    def delete(self, title=None, done=None):
        self.root.find_element(*self.__selectors["delete"]).wait().click()

    def mark_done(self):
        self.root.find_element(*self.__selectors["mark_done"]).wait().click()
        self.root.find_element(*self.__selectors["mark_in_progress"]).wait()
        assert self.done is True

    def mark_in_progress(self):
        self.root.find_element(*self.__selectors["mark_in_progress"]).wait().click()
        self.root.find_element(*self.__selectors["mark_done"]).wait()
        assert self.done is False
