from ping3 import ping as _ping
from statistics import mean, median
from time import sleep
from time import time
from threading import Thread

from datetime import datetime
from pypattyrn.behavioral.null import Null

from rich.console import Console
from ping_stat.logging import LOG_DEVICE
from ping_stat.utils.workers import PingWorker
from ping_stat.utils.network import Ping

console = Console()




# def ping_monitor(ping_object):
#     global monitoring
#
#     if not monitoring:
#         monitoring = True
#
#     p = ping_object
#
#     hist_len = 0
#
#     while monitoring:
#         h_len = len(p.history)
#         if h_len > hist_len:
#             hist_len = h_len
#             print(f'Last ping time: {p.latest}, Average ping time: {mean(p.history[-1][-1])}')
#         sleep(.3)








def monitor_mean(ping_object):
    global monitor_mean

    if not monitor_mean:
        monitor_mean = True

    while monitor_mean:
        sleep(.5)
        ping = ping_object
        hist = ping.history[-1][-1]
        print(f'Mean: {mean(hist)}')




        
    
