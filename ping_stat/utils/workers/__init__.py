"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.tech
Created: 5/9/2023 @ 4:05 PM
File:
  Name: __init__.py
  Filepath: ping_stat/utils/workers
"""
import datetime
import threading
import time
from time import sleep
from rich.console import Console
from typing import Optional, Union, Type, TypeVar
from ping_stat.errors import \
    RedundantWorkOrderError, \
    WorkerAlreadyStartedError, \
    WorkerNotStartedError
from statistics import mean, median
from ping_stat.utils import get_ping_mean

console = Console()
PING = TypeVar('PING')


class PingMonitor:
    def __init__(self, ping_object):
        self.ping_object = ping_object
        self.hist_len = 0
        self.last_avg = 0
        self.monitoring = False

        self.__thread = None


    @property
    def thread(self):
        return self.__thread


    def start(self):
        if self.monitoring:
            return
        self.monitoring = True
        thread = threading.Thread(target=self._monitor, daemon=True)
        self.__thread = thread
        thread.start()

    def stop(self):
        self.monitoring = False

    def _monitor(self):
        while self.monitoring:
            time.sleep(0.3)
            h_len = len(self.ping_object.history)
            if h_len > self.hist_len:
                self.hist_len = h_len

                current_avg = get_ping_mean(self)
                try:
                    last_ping = self.history[-2][-1][-1]
                except IndexError:
                    last_ping = 0

                if self.latest is None:
                    console.print('')

                cur_style = 'green' if last_ping > mean(self.latest) else 'red'
                avg_style = 'green' if current_avg < self.last_avg else 'red'
                console.print(
                    f'[bold]Last ping time: [/][{cur_style}]{self.ping_object.latest[-1]}[/]'
                    f'[bold] | Average ping time: [/][{avg_style}]{current_avg}[/]'
                )
                self.last_avg = current_avg

    @property
    def history(self):
        return self.ping_object.history

    @property
    def latest(self):
        return self.ping_object.latest

    @property
    def status(self):
        return {
            'monitoring': self.monitoring,
            'last_avg': self.last_avg,
            'hist_len': self.hist_len
        }

    def __repr__(self):
        status = self.status
        if status['monitoring']:
            return f'<PingMonitor: monitoring, last_avg={status["last_avg"]}, hist_len={status["hist_len"]}>'
        else:
            return '<PingMonitor: not monitoring>'





class PingWorker:
    def __init__(self, ping_object: PING, auto_create=True):
        self.__started: Optional[Union[None, datetime.datetime]] = None
        self.__thread: Optional[Union[None, threading.Thread]] = None

        self.__ping_object = None
        self.ping_object = ping_object
        self.ping = self.ping_object.ping

        if auto_create:
            self.__thread = self.create()

    @property
    def history(self):
        return self.ping_object.history

    @property
    def interval(self):
        return self.ping_object.interval

    @property
    def monitoring(self):
        return self.ping_object.monitoring

    @monitoring.setter
    def monitoring(self, new):
        self.ping_object.monitoring = new

    @property
    def ping_object(self) -> PING:
        return self.__ping_object

    @ping_object.setter
    def ping_object(self, new: Type[PING]) -> None:
        self.__ping_object = new

    @property
    def thread(self) -> threading.Thread:
        return self.__thread

    @thread.setter
    def thread(self, new):
        if not isinstance(new, threading.Thread):
            raise TypeError('"thread" must be of type "threading.Thread"')
        self.__thread = new

    @property
    def target(self):
        return self.ping_object.target

    @property
    def started(self) -> Optional[Union[None, datetime.datetime]]:
        return self.__started

    @started.setter
    def started(self, new: Optional[Union[None, datetime.datetime]]) -> None:
        if not isinstance(new, datetime.datetime):
            raise TypeError('"started" must be a datetime object')
        self.__started = new

    @property
    def status(self):
        if not self.thread:
            return {'running': False, 'started': self.started or False}
        elif self.thread.is_alive():
            return {'running': True, 'started': self.started or False, 'runtime': datetime.datetime.now() -
                                                                                  self.started}
        else:
            stopped_at = datetime.datetime.now() if self.started else None
            runtime = self.thread.join() if self.thread and self.thread.is_alive() else None
            return {'running': False, 'started': self.started, 'stopped_at': stopped_at, 'runtime': runtime}

    def create(self):
        """
        Create a new thread for the worker.

        Raises:
            RedundantWorkOrderError: If the worker already has a thread.

        Returns:
            threading.Thread: The new thread.
        """
        if self.thread:
            raise RedundantWorkOrderError(self.__class__.__name__)

        self.thread = threading.Thread(target=self.worker, daemon=True)
        return self.thread

    def start(self):
        """
        Start the worker's thread.

        Raises:
            WorkerAlreadyStartedError: If the worker's thread is already running.
        """
        if self.started:
            raise WorkerAlreadyStartedError(self.thread.name, str(self))
        self.monitoring = True
        self.thread.start()
        self.started = datetime.datetime.now()

    def stop(self):
        if not self.started:
            raise WorkerNotStartedError(self.thread.name, str(self))

        self.monitoring = False

        self.thread.join()

    def worker(self):
        """
        The worker's main loop.

        This method runs in the worker's thread and repeatedly pings the target at the specified interval, adding the
        ping results to the worker's history.

        Note:
            This method should not be called directly; instead, it should be run in a separate thread using the `start` method.

        """
        self.ping_object.monitoring = True
        while self.monitoring:
            sleep(self.interval)
            self.history.append(
                (
                    str(datetime.datetime.fromtimestamp(time.time()).isoformat()),
                    self.target,
                    self.ping()
                )
            )

    def __repr__(self):
        status = self.status
        if status['running']:
            return f'<PingWorker: running for {status["runtime"]}>'
        elif status['started']:
            return f'<PingWorker: started at {status["started"].strftime("%Y-%m-%d %H:%M:%S")}, stopped at {status["stopped_at"].strftime("%Y-%m-%d %H:%M:%S")}, ran for {status["runtime"]}>'
        else:
            return '<PingWorker: not started>'






"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
