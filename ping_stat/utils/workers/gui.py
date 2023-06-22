"""
Project: PingPing
Author: Inspyre Softworks - https://inspyre.techCreated: 6/1/2023 @ 4:27 PM
File:
  Name: gui
  Filepath: ping_stat/utils/workers
"""
import threading


class PingMonitorGUI:
    def __init__(self, ping_object):
        self.__ping_object = ping_object


    def setup_gui(self):
        layout = [[sg.Button(size=(2, 1), key=(i,j)) for j in range(10)] for i in range(10)]
        # Create the window
        self.window = sg.Window('Ping Monitor', layout)

    def update_gui(self, last_ping):
        # Update the GUI
        color = 'red' if last_ping > mean(self.latest) else 'green'
        button = self.window[(self.hist_len % 10, self.hist_len // 10)]
        button.update(button_color=('white', color))

    def _monitor(self):
        while self.monitoring:
            ...
            # After updating the statistics, update the GUI
            self.update_gui(last_ping)
            # Event loop for the window
            event, values = self.window.read(timeout=10)
            if event == sg.WINDOW_CLOSED:
                break

    def stop(self):
        self.monitoring = False
        self.window.close()


"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
