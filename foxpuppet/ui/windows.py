# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.foxpuppet import FoxPuppet


class Windows(FoxPuppet):

    def __init__(self, foxpuppet):
        self.selenium = foxpuppet.selenium

    @property
    def all(self):
        return self.selenium.window_handles

    @property
    def current(self):
        return self.selenium.current_window_handle

    def focus(self, handle):
        return self.selenium.switch_to.window(handle)

    def get_window_handle(self, title):
        if self.selenium.get_title() == title:
            self.selenium.switch_to.window(title)
            handle = self.current

        return handle
