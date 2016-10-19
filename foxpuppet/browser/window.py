# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.windows import Windows
from selenium.webdriver.common.by import By

from .navbar import Navbar
from .tabbar import Tabbar


class BrowserWindow(object):
    _file_menu_button_locator = (By.ID, 'file-menu')
    _file_menu_private_window_locator = (By.ID, 'menu_newPrivateWindow')
    _file_menu_new_window_button_locator = (By.ID, 'menu_newNavigator')
    _nav_bar_locator = (By.ID, 'nav-bar')
    _tab_browser_locator = (By.ID, 'tabbrowser-tabs')
    _title_bar_close_button_locator = (By.ID, 'titlebar-close')
    _title_bar_minimize_button_locator = (By.ID, 'titlebar-min')
    _title_bar_maximize_button_locator = (By.ID, 'titlebar-max')

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self.windows = Windows(selenium)
        self.navbar = Navbar(selenium)
        self.tabbar = Tabbar(selenium)

    @property
    def _navbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._navbar:
            navbar = self.selenium.find_element(*self._nav_bar_locator)
            return Navbar(self.selenium, navbar)
        return self._navbar

    @property
    def _tabbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._tabbar:
            tabbrowser = self.selenium.find_element(*self._tab_browser_locator)
            return Tabbar(self.selenium, tabbrowser)
        return self._tabbar

    @property
    def is_private(self):
        """Returns True if this is a Private Browsing window."""

        self.selenium.set_context('chrome')
        return self.selenium.execute_script("""
                Components.utils.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

                let chromeWindow = arguments[0].ownerDocument.defaultView;
                return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
            """, self.windows.window_element)

    def open_window(self, private=False):
        self.selenium.set_context('chrome')
        self.selenium.find_element(*self._file_menu_button_locator).click()
        if private:
            self.selenium.find_element(
                *self._file_menu_private_window_locator).click()
        else:
            self.selenium.find_element(
                *self._file_menu_new_window_button_locator).click()

    def close(self):
        self.selenium.close()

    def minimize(self):
        button = self.selenium.find_element(*self._title_bar_minimize_button_locator)
        button.click()

    def maximize(self):
        self.selenium.maximize()
