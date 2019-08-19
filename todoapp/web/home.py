# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from .base import BasePage
from .task import TaskBoardPage


class HomePage(BasePage):
    """The web app entry point
    """

    __selectors = {
        "navbar": (By.ID, "navbar"),
        "username": (By.NAME, "username"),
        "password": (By.NAME, "password"),
        "signin": (By.CLASS_NAME, "btn-success"),
        "signout": (By.CLASS_NAME, "btn-primary"),
        "taskboard": (By.CSS_SELECTOR, "#content table"),
    }

    def sign_in(self, username, password):
        """Sign in

        Arguments:
            username {str} -- the username
            password {str} -- the password

        Raises:
            WebDriverException: unable to sign in or sign in fail
        """
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
        """Sign out

        Raises:
            WebDriverException: unable to sign out or sign out fail
        """
        navbar_elt = self.driver.find_element(*self.__selectors["navbar"])
        navbar_elt.find_element(*self.__selectors["signout"]).wait().click()
        navbar_elt.find_element(*self.__selectors["signin"]).wait()

    @property
    def me(self):
        """Get user information

        Returns:
            str -- the username if connected, None otherwise

        Raises:
            WebDriverException: unable to get user information
        """
        navbar_elt = self.driver.find_element(*self.__selectors["navbar"])
        signout_elt = navbar_elt.find_element(*self.__selectors["signout"])
        if signout_elt.is_displayed():
            return signout_elt.find_element_by_tag_name("span").text
        else:
            return None

    @property
    def taskboard(self):
        """Get the taskboard

        Returns:
            TaskBoardPage -- the taskboard

        Raises:
            WebDriverException: no taskboard found
        """
        return TaskBoardPage(
            self.base_url,
            self.driver,
            self.driver.find_element(*self.__selectors["taskboard"]),
        )
