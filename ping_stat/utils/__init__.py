"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 2/23/2023 @ 9:03 AM
File:
  Name: __init__.py
  Filepath: ping_stat/utils
"""
from inspy_logger import InspyLogger
import time
from ping3 import ping, verbose_ping
from ping_stat.logging import add_child as add_child_logger, PROG_NAME
from rich.logging import RichHandler
import inspect
from ping_stat.utils.decorators import validate_properties
from statistics import mean, median


try:
    _ = LOGGER

except (ModuleNotFoundError, NameError) as e:
    LOGGER = add_child_logger(f'{PROG_NAME}.utils')
    LOGGER.debug(f'Loading {LOGGER.name}')


def get_ping_mean(ping_object, *args, **kwargs):
    times = gather_times(ping_object, *args, return_fail_list=False, **kwargs)
    p_means = [mean(p_time) for p_time in times if p_time]
    return mean(p_means)


def gather_times(
        ping_object,
        count_timeout_time_for_fails=True,
        timeout=5,
        return_success_list=True,
        return_fail_list=True,
        format_fail_times=True
):
    ping = ping_object
    ping_times = []
    failed_pings = []
    history = ping.history
    print(f'ping.history has {len(history)} entries.')
    for item in ping.history:

        if item[2] is None:
            failed_pings.append(item)
            if count_timeout_time_for_fails:
                ping_times.append(timeout)
        else:
            ping_times.append(item[2])

    if failed_pings:
        if len(failed_pings) >= 2:
            noun = 'pings'
        elif len(failed_pings) == 1:
            noun = 'ping'

        print(f'WARNING: Found {len(failed_pings)} failed {noun}')

    ret = ()
    if return_success_list:
        ret = (*ret, ping_times)
    if return_fail_list:
        ret = (*ret, failed_pings)

    if len(ret) == 1:
        ret = ret[0]

    return ret



class TTLTest:
    __auto_run: bool = False
    __end_at = None
    __history = []
    __iterations = 5
    __min_ttl = None
    __starting_at = 0
    __address = 'inspyre.tech'
    __timeout = 3

    def __init__(
            self,
            address=__address,
            auto_run=__auto_run,
            iterations=__iterations,
            timeout=__timeout,
            starting_at=__starting_at,
            end_at=__end_at
    ):
        self.address = str(address)
        self.auto_run: bool = auto_run
        self.end_at = end_at
        self.iterations = iterations
        self.starting_at = starting_at
        self.timeout = timeout

        if self.auto_run:
            self.run()

    @property
    def auto_run(self) -> bool:
        return self.__auto_run

    @auto_run.setter
    def auto_run(self, new: bool):
        self.__auto_run = new

    @property
    def iterations(self):
        return self.__iterations

    @iterations.setter
    def iterations(self, new):
        if not isinstance(new, int):
            raise TypeError('iterations must be an integer')

        self.__iterations = new

    @iterations.deleter
    def iterations(self):
        self.__iterations = 5

    @property
    def history(self):
        return self.__history

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, new):
        if not isinstance(new, (int, float)):
            raise TypeError('Timeout must be a number.')
        self.__timeout = new

    @timeout.deleter
    def timeout(self):
        self.__timeout = 3

    @property
    def address(self) -> str:
        return str(self.__test_addr)

    @address.setter
    def address(self, new):
        print(dir(new))
        print(type(new))
        if not isinstance(new, str):
            raise TypeError('Address must be a string!')
        self.__test_addr = new

    @address.deleter
    def address(self):
        self.__test_addr = 'inspyre.tech'

    @property
    def minimum_ttl(self):
        return self.__min_ttl

    @minimum_ttl.setter
    def minimum_ttl(self, new):
        if not isinstance(new, (int, None)):
            raise TypeError('minimum__ttl must be an integer')

        self.__min_ttl = new

    @minimum_ttl.deleter
    def minimum_ttl(self):
        self.minimum_ttl = None

    @property
    def starting_at(self) -> int:
        return self.__starting_at

    @starting_at.setter
    def starting_at(self, new):
        if not isinstance(new, int):
            raise TypeError('"starting_at" must be an integer')

        self.__starting_at = new


    def get_property_list(self):
        return [name for name, value in inspect.getmembers(TTLTest) if isinstance(value, property)]

    def run(self, address=None, timeout=None, starting_at=None):
        addr = address or self.address

        if addr != self.address:
            self.address = addr

        timeout = timeout or self.timeout

        if timeout != self.timeout:
            self.timeout = timeout

        cur_ttl = (starting_at or self.starting_at) - 1

        markA = time.time()

        while self.minimum_ttl in [None, 0]:
            cur_ttl += 1
            mark1 = time.time()
            print('Trying')
            res = ping(self.address, timeout=self.timeout, ttl=cur_ttl)
            print(f'Result: {res or "TIMEOUT"}')
            mark2 = time.time()
            if res:
                self.minimum_ttl = cur_ttl
                self.__history.append(f'FOUND:{self.minimum_ttl}')
            else:
                self.__history.append(f'TIMEOUT - {mark2 - mark1}')

        markB = time.time()

        tries = len(self.history)
        for item in self.history:
            if item.startswith('FOUND'):
                tries -= 1

        print(f'{markB - markA} seconds elapsed total. In {len(self.__history)} tries.')


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
