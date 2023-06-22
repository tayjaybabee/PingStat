"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 5/9/2023 @ 9:00 PM
File:
  Name: errors
  Filepath: ping_stat
"""
from ping_stat.errors.utils import get_caller_module_name, \
                                   get_caller_filename, \
                                   get_caller_line_number, \
                                   get_caller_function_name, \
                                   get_caller_class_name


class PingPingError(Exception):
    """Base class for all custom exceptions in the PingPing program."""

    def __init__(self, message: str = None):
        if get_caller_class_name() == 'PingPingGUIError':
            message = "An error occurred in the PingPing GUI"
        if message is None:
            message = "An error occurred in the PingPing program"
        super().__init__(message)


class RedundantWorkOrderError(PingPingError):
    """Exception raised when attempting to register a worker that already exists."""

    def __init__(self, worker_name: str, message: str = None):
        default_message = f"The specified worker already exists: {worker_name}"
        if message is not None:
            default_message += f". {message}"
        super().__init__(default_message)


class WorkerAlreadyStartedError(PingPingError):
    """Exception raised when attempting to start a worker that is already running."""

    def __init__(self, worker_name: str, message: str = None):
        default_message = f"The specified worker is already running: {worker_name}"
        if message is not None:
            default_message += f". {message}"
        super().__init__(default_message)


class WorkerNotStartedError(PingPingError):
    """Exception raised when attempting to stop a worker that is not running."""

    def __init__(self, worker_name: str, message: str = None):
        default_message = f"The specified worker is not running: {worker_name}"
        if message is not None:
            default_message += f". {message}"
        super().__init__(default_message)




"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
