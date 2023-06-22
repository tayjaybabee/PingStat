"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 2/27/2023 @ 3:55 AM
File:
  Name: helpers.py
  Filepath: ping_stat/utils
"""
from typing import Union, Tuple
from contextlib import contextmanager



def get_length_of_longest(target_list, with_string=False) -> Union[int, Tuple[int, str]]:
    """
    Get the length of the longest element in a list of strings or any other iterable.

    Args:
        target_list (list or iterable):
            A list or any other iterable to be searched for the longest element.

        with_string (bool, optional):
            Whether to return both the length of the longest element and the element itself.
            Defaults to False.

    Returns:
        int or tuple:
            If `with_string` is False, returns an integer representing the length of the longest element
        in the list. If `with_string` is True, returns a tuple of two values: the length of the longest element and
        the longest element itself.

    Raises:
        TypeError: If the input `target_list` is not an iterable or if any of its elements is not a string.

    Example:
        >>> get_length_of_longest(['a', 'bc', 'def'])
        3
        >>> get_length_of_longest(['a', 'bc', 'def'], with_string=True)
        (3, 'def')
        >>> get_length_of_longest(['a', 'bc', 123])
        TypeError: List elements must be strings.
    """
    longest_len = 0
    longest_entry = None
    for item in target_list:
        if len(item) > longest_len:
            longest_len = len(item)
            longest_entry = item
    return (longest_len, longest_entry) if with_string else longest_len


def calculate_mean(numbers):
    """
    Calculates the average of a list of numbers.

    Args:
        numbers (list of float or int): A list of numbers to calculate the average of.

    Returns:
        float: The average of the list of numbers.

    Raises:
        ValueError: If the input is an empty list.

    Example:
        >>> calculate_mean([1, 2, 3, 4, 5])
        3.0
    """
    if not numbers:
        raise ValueError("Input cannot be an empty list.")
    return sum(numbers) / len(numbers)


@contextmanager
def typeguard(typ):
    if not isinstance(typ, type):
        raise (TypeError(f'Expected a type, got {typ!r}'))
    try:
        yield
    except TypeError as e:
        raise TypeError(f'Type check failed: {typ.__name__} expected') from e



"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
