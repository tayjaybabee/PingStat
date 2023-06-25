# GitHub README for PingStat Project

## PingStat

PingStat is a Python-based utility for monitoring the latency of network connections by pinging a target IP address or hostname. This tool is designed to help network administrators, developers, and enthusiasts to evaluate the health and performance of network connections. Please use responsibly.

**⚠ Disclaimer:** Pinging a target is not a passive operation and may be detected by intrusion detection systems or firewall logs. Irresponsible use of this tool could potentially cause a denial of service to the target system's network services, or your own. Please use this tool only with the express permission of the target system's network administrator.

### Features

- **Customizability**: Set custom parameters for pinging, including the number of pings, timeout, interval, and packet size.
- **Continuous Monitoring**: Option to ping the target continuously and monitor the results in real time.
- **Rich Statistics**: Generates detailed reports including the number of successful and failed pings, as well as min, max, mean and average response times.
- **Threaded Workers**: Uses threaded workers for efficient pinging and monitoring.
- **CLI & GUI Mode**: Supports both command-line interface and graphical user interface modes.
- **Debug Mode**: Option to enable debug mode for extensive logging.

### Installation

PingStat requires Python 3.6 or newer. Clone the repository and install the required packages using pip.

```sh
git clone https://github.com/username/pingstat.git
cd pingstat
pip install -r requirements.txt
```

### Usage

#### Example Code:

```python
from ping_stat.main_class import Ping

# Initialize the Ping object with target and options
ping = Ping(target="google.com", auto_run=True, continuous_ping=False, timeout=5, runs=3)

# Perform the ping operation and get the results
results = ping.ping()

# Output the results
print(results)

# Generate a report of the ping operation
report = ping.generate_report()
print(report)
```

#### Command Line Usage:

A command line script might be included, for example:

```sh
python ping_stat.py --target google.com --runs 3 --timeout 5
```

### API Documentation

The main class is `Ping`. Here is a brief overview of its attributes and methods:

#### Attributes:

- `target (str)`: The IP address or hostname to ping.
- `auto_run (bool)`: Whether to automatically ping the target upon initialization.
- `timeout (float)`: The time in seconds to wait for a response before timing out.
- `runs (int)`: The number of times to send a ping request to the target.
- `interval (int)`: The time in seconds between ping attempts.
- `packet_size (int)`: Size of the packet payload in bytes.
- `continuous_ping (bool)`: Whether to ping the target continuously.
- `gui_mode (bool)`: Whether to use GUI mode.

#### Methods:

- `ping()`: Runs the ping operation and returns a list of ping times in milliseconds.
- `generate_report()`: Generates a detailed report of the ping operation.
- `start()`: Starts the ping operation if `continuous_ping` is True.
- `stop()`: Stops the continuous ping operation if running.

### Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License

PingStat is distributed under the MIT License. See the `LICENSE` file for more information.
