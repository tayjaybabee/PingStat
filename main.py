
from inspy_logger import InspyLogger
from ping_stat.config.arguments import ARGUMENTS, PROG_NAME
from ping_stat.utils import TTLTest
from ping_stat import Ping

LOG_LEVEL = ARGUMENTS.log_level

isl = InspyLogger(f'{PROG_NAME}', LOG_LEVEL)

if not isl.device.started:
    MOD_LOG = isl.device.start()
    MOD_LOG.debug(f'Logging started for {PROG_NAME}')

def main():
    log = isl.device.add_child(f'{PROG_NAME}.main')
    log.debug('Starting ping test...')
    ping = Ping(target=ARGUMENTS.target, auto_run=True, monitor_mode=True, interval=ARGUMENTS.interval)


if __name__ == '__main__':
    if (
        ARGUMENTS.subcommands
        and ARGUMENTS.subcommands.replace('-', '_').lower() == 'ttl_test'
    ):
        print('Received ttl test command')
        t_test = TTLTest()

    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
