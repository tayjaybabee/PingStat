"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 6/1/2023 @ 4:37 PM
File:
  Name: __init__.py
  Filepath: ping_stat/models/gui/windows
"""
import PySimpleGUI as sg
from ping_stat.models.gui.windows.errors import WindowAlreadyBuiltError


class MonitorWindow:
    def __init__(self, ping_object, auto_build=False, run_on_build=False):
        self.__layout = None

        self.__auto_build = None
        self.__built = False

        self.__run_on_build = None
        self.__running = False

        self.__started_ts = None

        self.__window = None

        self.auto_build = auto_build
        self.run_on_build = run_on_build

        if self.auto_build:
            self.__layout = self.build_layout()

    @property
    def auto_build(self) -> bool:
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, new):
        if not isinstance(new, bool):
            raise TypeError('"auto_build" must be of type "bool"')
        self.__auto_build = new

    @property
    def built(self) -> bool:
        return self.__built

    @property
    def layout(self):
        return self.__layout

    @property
    def run_on_build(self) -> bool:
        return self.__run_on_build

    @run_on_build.setter
    def run_on_build(self, new):
        if not isinstance(new, bool):
            raise TypeError('"run_on_build" must be of type "bool"')
        self.__run_on_build = new

    @property
    def running(self) -> bool:
        return self.__running

    @running.setter
    def running(self, new):
        if not isinstance(new, bool):
            raise TypeError('"running" must be of type "bool"')
        self.__running = new

    @property
    def started_timestamp(self) -> float:
        return self.__started_ts

    def build_layout(self):
        if self.layout is None:
            self.__layout = [[sg.Button(size=(2, 1), key=(i,j)) for j in range(10)] for i in range(10)]
        else:
            raise WindowAlreadyBuiltError()

        self.__built = True

        self.run()

    def run(self):
        if self.running:
            raise WindowAlreadyRunningError()
    




"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
