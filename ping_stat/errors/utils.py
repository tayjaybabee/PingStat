"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 6/1/2023 @ 5:10 PM
File:
  Name: utils
  Filepath: ping_stat/errors
"""
import inspect
import os


__all__ = [
    'get_caller_class_name',
    'get_caller_filename',
    'get_caller_function_name',
    'get_caller_line_number',
    'get_caller_module_name'
]


def get_caller_function_name():
    """
    Get the name of the calling function.

    Go two frames back in the stack: one for this function call, and one for the caller.
    Then, retrieve the name of the compiled function body from the code object.

    Returns:
        str: The name of the caller function.
    """
    # Go two frames back: one for this function call, and one for the caller
    return inspect.currentframe().f_back.f_back.f_code.co_name


def get_caller_filename():
    """
    Get the filename of the calling function.

    Go two frames back in the stack: one for this function call, and one for the caller.

    Returns:
        str: The filename of the caller function.
    """
    # Go two frames back: one for this function call, and one for the caller
    frame = inspect.currentframe().f_back.f_back
    return frame.f_globals['__file__']

def get_caller_line_number():
    """
    Get the line number of the calling function.

    Go two frames back in the stack: one for this function call, and one for the caller.
    Then, retrieve the line number from the frame.

    Returns:
        int: The line number of the caller function.
    """
    # Go two frames back: one for this function call, and one for the caller
    return inspect.currentframe().f_back.f_back.f_lineno


def get_caller_module_name():
    """
    Get the module name of the calling function.

    Go two frames back in the stack: one for this function call, and one for the caller.
    Then, get the module that contains the code of the frame.

    Returns:
        str: The name of the caller's module, or None if it couldn't be determined.
    """
    # Go two frames back: one for this function call, and one for the caller
    frame = inspect.currentframe().f_back.f_back
    module = inspect.getmodule(frame)
    return module.__name__ if module else None


def get_caller_class_name():
    """
   Get the name of the class of the calling function.

   Go two frames back in the stack: one for this function call, and one for the caller.
   Then, retrieve the class of the caller function from the frame.

   Returns:
       str: The name of the class of the caller function, or None if the function is not a method of a class.
   """
    # Go two frames back: one for this function call, and one for the caller
    frame = inspect.currentframe().f_back.f_back
    method = inspect.getframeinfo(frame).function
    instance = frame.f_locals.get('self')

    # Check if the function is a method of a class
    if instance and hasattr(instance, method):
        # Return the name of the class
        return instance.__class__.__name__
    else:
        return None



"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
