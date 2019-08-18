# -*- coding: utf-8 -*-


class BasePage(object):
    def __init__(self, driver, root=None):
        self.driver = driver
        self.root = root
