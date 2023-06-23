from inspy_logger import InspyLogger
from ping_stat.config.arguments import ARGUMENTS, PROG_NAME
from ping_stat.utils import TTLTest
from ping_stat import Ping
from time import sleep

LOG_LEVEL = ARGUMENTS.log_level

isl = InspyLogger(f'{PROG_NAME}', LOG_LEVEL)

if not isl.device.started:
    MOD_LOG = isl.device.start()
    MOD_LOG.debug(f'Logging started for {PROG_NAME}')

ping = None

def main():
    global ping
    log = isl.device.add_child(f'{PROG_NAME}.main')
    log.debug('Starting ping test...')

    ping = Ping(target=ARGUMENTS.target, auto_run=True, live_mode=True, continuous_ping=True, interval=ARGUMENTS.interval)

    try:
        while ping.monitoring:
            sleep(.3)
    except KeyboardInterrupt:
        print("Stopping ping monitoring...")
        ping.stop_monitoring()

if __name__ == '__main__':
    if (
            ARGUMENTS.subcommands
            and ARGUMENTS.subcommands.replace('-', '_').lower() == 'ttl_test'
    ):
        print('Received ttl test command')
        t_test = TTLTest()

    main()
