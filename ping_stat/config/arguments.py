"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.tech
Created: 2/23/2023 @ 9:08 AM
File:
  Name: arguments
  Filepath: ping_stat/config
"""
from argparse import ArgumentParser
from inspy_logger import LEVELS as LOG_LEVELS
from ping_stat.__about__ import __PROG__ as PROG_NAME, __DESCRIPTION__ as DESCRIPTION, __VERSION_FULL__ as VERSION


class PingPingArguments(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(PingPingArguments, self).__init__(*args, **kwargs)

        self.prog = PROG_NAME
        self.description = DESCRIPTION

        self.add_argument(
            '-l',
            '--log-level',
            help='Set the level at which to log messages. Defaults to INFO',
            choices=LOG_LEVELS,
            default='info',
            action='store',
            required=False
        )

        self.add_argument(
            '-i',
            '--interval',
            help='The time (in seconds) to wait between ping requests',
            default=3,
            type=int,
            action='store',
            required=False
        )

        self.add_argument(
            '--target',
            help='The target address to attempt to ping.',
            default='inspyre.tech',
            type=str,
            action='store',
            required=False
        )

        self.add_argument(
            '--timeout',
            help='The time (in seconds) to wait for connection to be established before giving up.',
            default=3,
            type=str,
            action='store',
            required=False

        )

        sub_parsers = self.add_subparsers(
            dest='subcommands',
            parser_class=ArgumentParser,
            title='Subcommands',
        )

        ttl_test_parser = sub_parsers.add_parser('TTL-Test', aliases=['ttl-test'])
        ttl_test_parser.description = 'Determines the minimum number of hops needed to reach the destination'

        ttl_test_parser.add_argument(
            '-s',
            '--starting-from',
            help='The TTL you want to start the test from.',
            default=1,
            type=int,
            action='store',
            required=False
        )

        ttl_test_parser.add_argument(
            '-e',
            '--end-at',
            help='Which number of TTL should we stop after. Default is 15',
            default=15,
            type=int,
            action='store',
            required=False
        )

        monitor_parser = sub_parsers.add_parser('monitor')
        monitor_parser.description = 'Monitor your ping-time against the specified host server.'

        monitor_parser.add_argument(
            '-i',
            '--interval',
            help='The time between ping requests',
            default=2,
            type=int,
            action='store',
            required=False

        )
        

args = PingPingArguments()
ARGUMENTS = args.parse_args()



"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

    - The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
  the Software.
    
    - THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
   THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
   SOFTWARE.
"""
