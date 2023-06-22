"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 2/27/2023 @ 4:37 AM
File:
  Name: decorators.py
  Filepath: ping_stat/utils
"""
import typing


def validate_properties(cls):
    for name, prop in cls.__dict__.items():
        if isinstance(prop, property) and prop.fset is not None:
            schema = {'value': typing.get_type_hints(cls)[name]}
            validator = Validator(schema)

            def setter(self, value, name=name, validator=validator):
                if not validator.validate({'value': value}):
                    raise ValueError(validator.errors)
                setattr(self, f"_{name}", value)

            setattr(cls, name, property(prop.fget, setter))

    return cls


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
