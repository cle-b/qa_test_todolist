# -*- coding: utf-8 -*-


class BasePage(object):
    def __init__(self, base_url, driver, root=None):
        self.driver = driver
        self.root = root
        self.base_url = base_url

    def homepage(self):
        self.driver.get(self.base_url)
