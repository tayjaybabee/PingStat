import logging


def is_number(string, force_integer=False, rounding=None):
    num = None

    print(f'Received string {string}')

    if isinstance(string, (int, float)):
        print('Detected that received string is actually an integer or float...')
        num = string
        print(f'Num is now "{num}" after detecting that "string" is indeed a string.')
    elif isinstance(string, str):
        print('Detected that received string is indeed a string.')

        try:
            print('Attempting to convert the string to a float...')
            # Try to convert the string to a float.
            num = float(string)
            print(f'After conversion attempt from string to float, {num} is {type(num)}')

            # If rounding is specified, round the number.
            if rounding is not None and isinstance(rounding, int) and rounding >= 0:
                print('Detected parameters to return the number rounded.')
                num = round(num, rounding)
                print(f'After rounding, the number is {num}')

        except ValueError as e:
            print(e)
            # If a ValueError is raised, the string is not a number.
            num = string

    if force_integer and not isinstance(num, str):
        print('Detecting that we were instructed to return an integer.')
        num = int(num)
        print(f'After converting the number to an integer it is now; {num}')

    print(f'Returning number which is {num}')
    return num


def translate_to_logging_level(level_str):
    """
    Translates a string to a ps_logging level for Python.

    Arguments:
        level_str (str, required):
            The string that you'd like converted to a log-level.

    """
    level_str = level_str.upper()

    # Mapping of string to ps_logging levels
    level_mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
        'NOTSET': logging.NOTSET
    }

    # Return the ps_logging level if it exists, else return None
    return level_mapping.get(level_str)
