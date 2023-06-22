"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 6/1/2023 @ 4:49 PM
File:
  Name: errors.py
  Filepath: ping_stat/models/gui/windows
"""
from ping_stat.errors import PingPingError


class PingPingGUIError(PingPingError):
    def __init__(self, message: str = None):
        default_message = "There has been a problem with the GUI"
        if message is not None:
            default_message += f". {message}"
        super().__init__(default_message)


class WindowAlreadyBuiltError(PingPingGUIError):
    def __init__(self, message: str = None):
        default_message = "This window is already built."
        if message is not None:
            default_message += f". {message}"
        super().__init__(default_message)


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
