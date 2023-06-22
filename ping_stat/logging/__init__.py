"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 2/26/2023 @ 1:34 AM
File:
  Name: __init__.py
  Filepath: ping_stat/logging
"""
from ping_stat.config.arguments import ARGUMENTS
from ping_stat.__about__ import __PROG__ as PROG_NAME
from inspy_logger import InspyLogger
from rich.logging import RichHandler


# Set up logging
ISL = InspyLogger(PROG_NAME, 'debug')

LOG_DEVICE = ISL.device

if not LOG_DEVICE.started:
    # LOG_DEVICE.addHandler(RichHandler(rich_tracebacks=True))
    LOGGER = LOG_DEVICE.start()
    LOGGER.debug(f'Logger started for {PROG_NAME}')

#log = LOG_DEVICE.add_child(f'{PROG_NAME}.logging')
LOGGER.debug(f'Logger started for {LOGGER.name}')


def add_child(name):
    _ = LOG_DEVICE.add_child(name)
    _.debug(f'Received logger {_.name}')

    return _


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
