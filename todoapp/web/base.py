# -*- coding: utf-8 -*-


class BasePage(object):
    username = ""  # for information only

    def __init__(self, base_url, driver, root=None):
        """Initialize the PageObject.

        Arguments:
            base_url {str} -- the landing page URL
            driver {WebDriver} -- the selenium web driver

        Keyword Arguments:
            root {WebElement} -- the root WebElement of the PageObject (default: {None})
        """
        self.driver = driver
        self.root = root
        self.base_url = base_url

    def homepage(self):
        """Navigate to the homepage
        """
        self.driver.get(self.base_url)
