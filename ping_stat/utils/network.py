"""
PingPing: network
Module Author: Inspyre Softworks (https://inspyre.tech)
Module Created: 5/9/2023 @ 8:47 PM
Module Path: ping_stat/utils

This module implements the network functionality for the PingPing project. It is responsible for performing
network operations, including the following:

1. Pinging operations on a specific target (IP address or hostname).
2. Generating network operation reports.
3. Managing the state and execution of the PingWorker and PingMonitor classes.

Classes:
- Ping: This class represents a ping operation on a target. It has several configurable parameters like
  target IP or hostname, timeout, and the number of times to perform the operation. It can also perform
  the operation automatically upon initialization.

Attributes:
- console: An instance of the rich.console.Console class for console operations.
- track_mean: A boolean value used for internal operations.

Usage:
from ping_stat.utils.network import Ping

# Create an instance of the Ping class, automatically performing the operation upon initialization.
ping = Ping(target="google.com", auto_run=True)

# Perform the operation manually and print the results.
print(ping.ping())

Disclaimer:
Please use this tool only with the express permission of the target system's network administrator and
exercise due care and responsibility in doing so. The author of this tool assumes no liability for any damage,
legal or otherwise, caused by its use. Pinging a target is not a passive operation and may be detected by
intrusion detection systems or firewall logs. Irresponsible use of this tool could potentially cause a
denial of service to the target system's network services, or your own.
"""
import netifaces
from ping3 import ping as _ping
from ping_stat.errors import RedundantWorkOrderError, WorkerAlreadyStartedError

from ping_stat.utils import gather_times
from ping_stat.utils.workers import PingMonitor, PingWorker
from pypattyrn.behavioral.null import Null
import queue
from rich.console import Console
from statistics import mean, median
from time import sleep, time
from ping_stat.ps_logging import add_child, Loggable
from ping_stat.ps_logging.helpers import is_number
import inspect


LOG_DEVICE = add_child('network')
MOD_LOG = LOG_DEVICE.logger
MOD_LOG.debug(f'Started logging for {MOD_LOG.name}')

console = Console()


track_mean = False


def get_gateway():
    """


    Returns:

    """
    log_name = 'get_gateway'
    full_log_name = f'{LOG_DEVICE.logger.name}.{log_name}'
    log_dev = LOG_DEVICE.get_child(log_name)
    log = log_dev.logger
    log.debug('Created')
    gateways = netifaces.gateways()
    return gateways['default'][netifaces.AF_INET][0]




class Ping(Loggable):
    """
    A class for performing ping operations on a target.

    Disclaimer:
        Please use this tool only with the express permission of the target system's network administrator,
        and exercise due care and responsibility in doing so. The author of this tool assumes no liability for any damage,
        legal or otherwise, caused by its use.

    Note:
        Pinging a target is not a passive operation and may be detected by intrusion detection systems or firewall logs.
        Irresponsible use of this tool could potentially cause a denial of service to the target system's network
        services, or your own.


    Attributes:
        target (str):
            The IP address or hostname to ping.

        auto_run (bool):
            Whether to automatically ping the ping operation upon initialization.

        timeout (float):
            The time in seconds to wait for a response before timing out.

        runs (int):
            The number of times to send a ping request to the target.

    Methods:
        ping():
            Runs the ping operation and returns a list of ping times (in milliseconds).

    Usage:
        ping = Ping(target="google.com", auto_run=True)
        ping.ping()
        # [15.132, 15.269, 15.265]
    """
    __cls_log = add_child('PingPing.Ping')

    __auto_run = False
    __target = None
    __timeout = 5
    __runs = 3
    __results = None
    __interval = 1
    __size = 256
    __history = []
    __monitoring = False
    __continuous_ping = False

    def __init__(
            self,
            target: str,
            parent_logging_device=LOG_DEVICE,
            auto_run=__auto_run,
            continuous_ping=None,
            timeout=__timeout,
            runs=__runs,
            interval=__interval,
            packet_size=__size,
            live_mode=None,
            debug_mode=False,
            gui_mode=False,
            **kwargs
    ):
        """
        Initializes the Ping object.

        Args:
            target (str):
                The IP address or hostname to ping.
            auto_run (bool):
                Whether to automatically ping the ping operation upon initialization.
            timeout (float):
                The time in seconds to wait for a response before timing out.
            runs (int):
                The number of times to send a ping request to the target.

        Raises:
            TypeError:
                If any argument is of the wrong type.
        """
        global monitoring
        super(Ping, self).__init__(parent_logging_device)
        func_log_device = parent_logging_device.get_child('Ping')
        log = func_log_device.logger

        self.runs = runs

        self.target = target
        log.debug(f'Ping target: {self.target}')

        self.auto_run = auto_run
        log.debug(f'Auto-run: {self.auto_run}')

        self.timeout = timeout
        log.debug(f'Timeout: {self.timeout}')

        self.__continuous_ping = continuous_ping
        log.debug(f'Monitor mode active: {self.continuous_ping}')

        self.interval = interval
        log.debug(f'Ping interval: {self.interval}')

        log.debug(f'{kwargs}')

        self.__debug_mode = debug_mode
        log.debug()

        self.__ping_worker = None

        self.__queue = None

        if self.__continuous_ping:
            self.__queue = queue.Queue()
            self.__ping_worker = self.create_worker()
            if live_mode is not None:
                self.live_mode = True
                self.ping_monitor = PingMonitor(self)

            else:
                self.live_mode = False

        else:
            self.__ping_worker = None

        # Configure packet size
        self.__packet_size = packet_size or self.__packet_size

        if self.auto_run:
            self.start()


    @property
    def argument_state(self):
        args = locals()
        args.pop('self')
        return args


    @property
    def auto_run(self) -> bool:
        """
        bool:
            Whether to automatically ping the ping operation upon initialization.
        """
        return self.__auto_run

    @auto_run.setter
    def auto_run(self, new: bool):
        """
        Sets the auto_run attribute.

        Args:
            new (bool):
                Whether to automatically ping the ping operation upon initialization.

        Raises:
            TypeError:
                If new is not a boolean.
        """
        if not isinstance(new, bool):
            raise TypeError('"auto_run" must be of type "bool".')

        self.__auto_run = new

    @property
    def interval(self) -> int:
        return self.__interval

    @interval.setter
    def interval(self, new):

        if not isinstance(new, int):
            new = is_number(new)
            if not new:
                raise TypeError('"interval" must be of type "int".')

        self.__interval = new

    @property
    def gui_mode(self) -> bool:
        return self.__gui_mode

    @gui_mode.setter
    def gui_mode(self, new):
        if not isinstance(new, bool):
            raise TypeError('"gui_mode" must be of type "bool".')
        self.__gui_mode = new

    @property
    def packet_size(self):
        return self.__size

    @packet_size.setter
    def packet_size(self, new):

        if not isinstance(new, int):
            raise TypeError("packet_size must be an integer!")

        if new <= 0:
            raise ValueError('packet_size must be a positive integer')

        self.__size = new

    @property
    def ping_worker(self):
        return self.__ping_worker

    @property
    def target(self):
        """
        str:
            The IP address or hostname to ping.
        """
        return self.__target

    @target.setter
    def target(self, new):
        """
        Sets the target attribute.

        Args:
            new (str):
                The IP address or hostname to ping.

        Raises:
            TypeError:
                If new is not a string.
            ValueError:
                If new is an empty string.
        """
        if not isinstance(new, str):
            raise TypeError('"target" must be a string')

        if not new:
            raise ValueError('"target" cannot be an empty string')

        self.__target = new

    @property
    def continuous_ping(self):
        return self.__continuous_ping

    @continuous_ping.setter
    def continuous_ping(self, new):
        if not isinstance(new, bool):
            raise TypeError('"new" must be of type bool!')

        self.__continuous_ping = new

    @property
    def monitoring(self):
        return self.__monitoring

    @monitoring.setter
    def monitoring(self, new):
        if not isinstance(new, bool):
            raise TypeError('"monitoring" must be of type bool"')

        self.__monitoring = new

    @property
    def history(self):
        return self.__history

    @history.setter
    def history(self, new):
        if not isinstance(new, list):
            raise TypeError('"new" must be of type list!')

    @property
    def latest(self):
        try:
            return self.history[-1][-1]
        except TypeError:
            return self.history

    @property
    def timeout(self) -> float:
        """
        float:
            The time in seconds to wait for a response before timing out.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, new):
        """
        Sets the timeout attribute.

        Args:
            new (float):
                The time in seconds to wait for a response before timing out.

        Raises:
            TypeError:
                If new is not a float or an integer.
            ValueError:
                If new is not positive.
        """
        if not isinstance(new, (int, float)):
            new = is_number(self.timeout)
            if not new:
                raise TypeError('"timeout" must be a float or an integer')

        if new <= 0:
            raise ValueError('"timeout" must be positive')

        self.__timeout = int(new)

    @property
    def queue(self):
        return self.__queue

    @queue.deleter
    def queue(self):
        self.__queue.empty()

    @property
    def results(self):
        return self.__results

    @property
    def runs(self):
        """
       int:
           The number of times to send a ping request to the target.
       """
        return self.__runs

    @runs.setter
    def runs(self, new):
        """
        Sets the runs attribute.

        Args:
            new (int):
                The number of times to send a ping request to the target.

        Raises:
            TypeError:
                If new is not an integer.
            ValueError:
                If new is not positive.
        """
        log_device = self.create_child_logger('PropSet:run')
        log = log_device.logger

        log.debug(f'Received new value of {new}')

        if not isinstance(new, int):
            raise TypeError("'runs' must be an integer!")

        log.debug('New value seems valid, setting...')

        if new <= 0:
            raise ValueError("'runs' must be positive")

        self.__runs = new

        log.debug(f'Value of Ping().runs: {self.__runs}')

    @runs.deleter
    def runs(self):
        """
        Resets the runs attribute to its default value.
        """
        self.__runs = 3

    @property
    def status(self):
        return {
            'continuous_mode': {
                'enabled': self.continuous_ping,
                'state': {'alive': bool(self.ping_worker.thread.is_alive())},
            }
        }

    def create_worker(self, reset=False):
        from ping_stat.utils.workers import PingWorker
        if self.ping_worker is not None and not reset:
            raise RedundantWorkOrderError('ping_worker', 'Try resetting the ping worker.')
        else:
            self.__ping_worker = PingWorker(self)

        return self.ping_worker


    def ping(self):
        """
        Runs the ping operation and returns a list of ping times (in milliseconds).

        Returns:
            list or float:

                - If the 'runs' attribute is greater than 1, returns a list of ping times (in milliseconds).

                - If the 'runs' attribute is 1, returns a single ping time (in milliseconds).

        Raises:
            PingError:
                If the ping operation failed.

        """

        # pings = [
        #     _ping(self.target, size=256, timeout=self.timeout)
        #     for _ in range(self.runs)
        # ]
        pings = []
        log_device = self.log_device.get_child('PingPing.Ping.ping')
        log = log_device.logger

        for _ in range(self.runs):

            log.debug(f'({_ + 1} of {self.runs}) - Pinging {self.target} with a payload of {self.packet_size} bytes and'
                      f' a timeout of {self.timeout}.')


            # Ping the target with the given parameters and app end this
            # to the list of ping results.
            ping_res = _ping(
                self.target,
                size=self.packet_size,
                timeout=int(self.timeout)
            )
            pings.append(ping_res or self.timeout)

            sleep(self.interval)

        if len(pings) == 1:
            pings = pings[0]

        self.__results = pings

        return pings



    def generate_report(self):
        successful, failed = gather_times(self, count_timeout_time_for_fails=True)
        num_successful = len(successful)
        num_failed = len(failed)
        ping_mean = mean(successful)
        max_time = max(successful)
        min_time = min(successful)

        return {
            'pings_returned': num_successful,
            'pings_failed': num_failed,
            'wait_time': {
                'min': min_time,
                'max': max_time,
                'mean': ping_mean,
                'average': sum(successful)
            },
        }

    def start(self):
        global monitoring

        if self.continuous_ping:
            if self.ping_worker.status['started']:
                raise WorkerAlreadyStartedError(self.ping_worker.thread.name)

            self.ping_worker.start()

            if self.live_mode:
                self.monitoring = True
                self.ping_monitor.start()


    def stop_monitoring(self):
        global monitoring
        monitoring = False
        self.ping_monitor.stop()
        self.ping_monitor.thread.join()

    def stop(self):
        if self.live_mode:
            self.stop_monitoring()

        self.monitoring = False
        self.ping_worker.join()


    def __is_member__(self):
        log_device = self.log_device.get_child('__is_member__')
        log = log_device.logger

        current_frame = inspect.currentframe()
        log.debug(f'Current frame: {current_frame}')

        caller_frame = current_frame.f_back
        log.debug(f'Caller frame: {caller_frame}')

        caller_self = caller_frame.f_locals.get('self', None)
        log.debug(f'Caller self: {caller_self}')

        log.debug('Checking if caller is a member of this class...')
        if not isinstance(caller_self, Ping):
            raise PermissionError(
                'Access denied.\n'
                f'Method can only be accessed by members of the same class. {caller_self.__name__} is not such a member')

        log.debug(f'Access granted to {caller_self.__class__.__name__}')


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
