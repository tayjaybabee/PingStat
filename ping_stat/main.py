from ping_stat.config.arguments import PROG_NAME, PingPingArguments
from ping_stat.utils import TTLTest
from ping_stat import Ping
from ping_stat.ps_logging import LOG_DEVICE, add_child
from time import sleep
import sys


ARGUMENTS = PingPingArguments()


mod_log_device = add_child('main')
mod_log = mod_log_device.logger
mod_log.debug('Initialized logger')

ping = None

num_cycles = 0



def main():
    global ping
    log_device = mod_log_device.get_child('main')
    log = log_device.logger
    log.debug('Starting ping test...')

    ping = Ping(target=ARGUMENTS.target, auto_run=True, live_mode=True, continuous_ping=True, interval=ARGUMENTS.interval)

    log.debug('Initialized Ping class')

    try:
        log.debug('Entering main program loop.')
        print('Press Ctrl+C to quit.')
        while ping.monitoring:
            sleep(.3)
    except KeyboardInterrupt:
        print("Stopping ping monitoring...")
        ping.stop_monitoring()

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        pass
    else:
        try:
            if (
                    ARGUMENTS.subcommands
                    and ARGUMENTS.subcommands.replace('-', '_').lower() == 'ttl_test'
            ):
                print('Received ttl test command')
                t_test = TTLTest()
        except AttributeError as e:
            mod_log.warning(e)


    main()
