# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from .base import BasePage
from .task import TaskBoardPage


class HomePage(BasePage):

    __selectors = {
        "navbar": (By.ID, "navbar"),
        "username": (By.NAME, "username"),
        "password": (By.NAME, "password"),
        "signin": (By.CLASS_NAME, "btn-success"),
        "signout": (By.CLASS_NAME, "btn-primary"),
        "taskboard": (By.CSS_SELECTOR, "#content table"),
    }

    def sign_in(self, username, password):
        navbar_elt = self.driver.find_element(*self.__selectors["navbar"])
        username_elt = navbar_elt.find_element(*self.__selectors["username"]).wait()
        username_elt.clear()
        username_elt.send_keys(username)
        password_elt = navbar_elt.find_element(*self.__selectors["password"]).wait()
        password_elt.clear()
        password_elt.send_keys(password)
        navbar_elt.find_element(*self.__selectors["signin"]).click()
        navbar_elt.find_element(*self.__selectors["signout"]).wait()

    def sign_out(self):
        navbar_elt = self.driver.find_element(*self.__selectors["navbar"])
        navbar_elt.find_element(*self.__selectors["signout"]).wait().click()
        navbar_elt.find_element(*self.__selectors["signin"]).wait()

    @property
    def me(self):
        navbar_elt = self.driver.find_element(*self.__selectors["navbar"])
        signout_elt = navbar_elt.find_element(*self.__selectors["signout"])
        if signout_elt.is_displayed():
            return signout_elt.find_element_by_tag_name("span").text
        else:
            return None

    @property
    def taskboard(self):
        return TaskBoardPage(
            self.driver, self.driver.find_element(*self.__selectors["taskboard"])
        )
