"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 2/26/2023 @ 1:34 AM
File:
  Name: __init__.py
  Filepath: ping_stat/ps_logging
"""
# from ping_stat.__about__ import __PROG__ as PROG_NAME
# from inspy_logger import InspyLogger
# from rich.ps_logging import RichHandler
#
#
# # Set up ps_logging
# ISL = InspyLogger(PROG_NAME, 'debug')
#
# LOG_DEVICE = ISL.device
#
# if not LOG_DEVICE.started:
#     # LOG_DEVICE.addHandler(RichHandler(rich_tracebacks=True))
#     LOGGER = LOG_DEVICE.start()
#     LOGGER.debug(f'Logger started for {PROG_NAME}')
#
# #log = LOG_DEVICE.add_child(f'{PROG_NAME}.ps_logging')
# LOGGER.debug(f'Logger started for {LOGGER.name}')
#
#
# def add_child(name):
#     _ = LOG_DEVICE.add_child(name)
#     _.debug(f'Received logger {_.name}')
#
#     return _
import inspect
import logging
from rich.logging import RichHandler
from ping_stat.__about__ import __PROG__ as PROG_NAME
from ping_stat.ps_logging.helpers import translate_to_logging_level as str_to_logging_level


DEFAULT_LOGGING_LEVEL = logging.DEBUG




class Logger:
    """
    A Singleton class for managing application logging. Handles logging to both the console and a file.

    Attributes:
         instances (dict): A dictionary to store instances of each logger.
    """

    instances = {}

    def __new__(cls, name, *args, **kwargs):
        """
        Implements Singleton pattern, ensuring only one instance of Logger with a given name.

        Parameters:
            name (str): The name of the logger.

        Returns:
            Logger: An instance of the Logger class.
        """
        if name not in cls.instances:
            instance = super(Logger, cls).__new__(cls)
            cls.instances[name] = instance
            return instance
        return cls.instances[name]

    def __init__(self, name, console_level=DEFAULT_LOGGING_LEVEL, file_level=logging.DEBUG, filename='app.log'):
        """
        Initializes a logger instance. Sets up console and file handlers and establishes logging levels.

        Parameters:
            name (str):
                The name of the logger.

            console_level (logging level object, optional):
                The logging level for the console. Defaults to DEBUG.
                Must be a member of logging module's set of level constants (like logging.INFO or logging.DEBUG).

            file_level (logging level object, optional):
                The logging level for the file. Defaults to DEBUG.
                Must be a member of logging module's set of level constants (like logging.INFO or logging.DEBUG).

            filename (str, optional): The name of the log file. Defaults to 'app.log'.
        """
        if not hasattr(self, 'logger'):
            self.__name = name
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)
            self.__console_level = console_level
            self.filename = filename
            self.__file_level = file_level or DEFAULT_LOGGING_LEVEL

            # Remove existing handlers
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)

            # Prevent log records from being passed to the handlers of ancestor loggers.
            self.logger.propagate = False

            self.set_up_console()
            self.set_up_file()
            self.children = []

    def set_up_console(self):
        """
        Sets up console logging for the logger. Uses RichHandler for a rich, colored output.
        """
        console_handler = RichHandler(show_level=True, markup=True, rich_tracebacks=True, tracebacks_show_locals=True,)
        formatter = logging.Formatter('[green][bold][%(name)s][bold][/green] - %(message)s')

        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.__console_level)
        self.logger.addHandler(console_handler)

    def set_up_file(self):
        """
        Sets up file logging for the logger. Writes log entries to the file specified at initialization.
        """
        file_handler = logging.FileHandler(self.filename)
        file_handler.setLevel(self.__file_level)
        formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_level(self, console_level=None, file_level=None):
        """
        Sets the logging levels for the logger and its child loggers.

        Parameters:
            console_level (logging level object, optional): The console logging level.
                Must be a member of logging module's set of level constants (like logging.INFO or logging.DEBUG).
            file_level (logging level object, optional): The file logging level.
                Must be a member of logging module's set of level constants (like logging.INFO or logging.DEBUG).
        """
        if console_level is not None:
            self.logger.handlers[0].setLevel(console_level)
            for child in self.children:
                child.set_level(console_level=console_level)

        if file_level is not None:
            self.logger.handlers[1].setLevel(file_level)
            for child in self.children:
                child.set_level(file_level=file_level)

    def get_child(self, name=None, console_level=None, file_level=None):
        console_level = console_level or DEFAULT_LOGGING_LEVEL
        # If no name is provided, use the name of the calling function
        if name is None:
            # Get the stack frame of the caller
            caller_frame = inspect.stack()[1]
            # Get the name of the calling function
            name = caller_frame.function

        child_logger_name = f'{self.logger.name}.{name}'

        # Check if child logger already exists
        for child in self.children:
            if child.logger.name == child_logger_name:
                return child

        # If child logger doesn't exist, create a new one
        child_logger = Logger(child_logger_name, console_level, file_level)
        self.children.append(child_logger)
        return child_logger

    def get_child_names(self):
        """
        Returns the names of all child loggers of this logger.

        Returns:
            list of str: A list of names of the child loggers.
        """
        children_names = []

        for child in self.children:
            children_names.append(child.logger.name)

        return children_names

    def find_child_by_name(self, name: str, ):
        names = self.get_child_names()



LOG_DEVICE = Logger(PROG_NAME,DEFAULT_LOGGING_LEVEL)
MOD_LOG_DEVICE = LOG_DEVICE.get_child(__name__)
MOD_LOGGER = MOD_LOG_DEVICE.logger
MOD_LOGGER.debug(f'Started logger for {__name__}.')

add_child = LOG_DEVICE.get_child


class Loggable:
    """
    A meta-class for loggable classes.
    Provides logging capabilities to the classes that inherit from it.
    """

    def __init__(self, parent_logging_device):
        """
        Initializes the Loggable object, creating a child logger for this instance.

        Parameters:
            parent_logging_device (Logger): The parent Logger device from which this object's logger will be derived.
        """
        self.__log_name = self.__class__.__name__

        self.__parent_log_device = parent_logging_device
        self.log_device = parent_logging_device.get_child(self.__class__.__name__)

    @property
    def parent_log_device(self):
        """ The parent logging device. """
        return self.__parent_log_device

    def create_child_logger(self, name=None, override=False):
        """
        Creates and returns a child logger of this object's logger.

        Parameters:
            name (str, optional): The name of the child logger.
                If not provided, the name of the calling function is used.
            override (bool, optional): A flag to override the membership check. Defaults to False.

        Returns:
            Logger: An instance of the Logger class that represents the child logger.
        """
        if not override:
            self.__is_member__()

        if name is None:
            name = inspect.stack()[1][3]  # Get the name of the calling function if no name is provided

        return self.log_device.get_child(name)

    def __is_member__(self):
        """
        Checks whether the caller of this method is a member of the same class.

        Raises:
            PermissionError: If the caller of this method is not a member of the same class.
        """
        log_device = self.log_device.get_child('__is_member__')
        log = log_device.logger

        current_frame = inspect.currentframe()
        log.debug(f'Current frame: {current_frame}')

        caller_frame = current_frame.f_back
        log.debug(f'Caller frame: {caller_frame}')

        caller_self = caller_frame.f_locals.get('self', None)
        log.debug(f'Caller self: {caller_self}')

        log.debug('Checking if caller is a member of this class...')
        if not isinstance(caller_self, self.__class__):
            raise PermissionError(
                'Access denied.\n'
                f'Method can only be accessed by members of the same class. {caller_self.__class__.__name__} is not such a member')

        log.debug(f'Access granted to {caller_self.__class__.__name__}')


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
