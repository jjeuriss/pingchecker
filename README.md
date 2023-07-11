# Ping Checker

Ping Checker is a Python script that performs continuous pinging to a specified IP address and exposes the ping statistics as Prometheus metrics. The script uses the `ping` command on a Linux PC to send pings at regular intervals and collects metrics such as packet loss, latency (min, avg, max), and the number of packets transmitted and received

![image](https://github.com/jjeuriss/pingexporter/assets/20801240/6c46907d-aae4-4479-9098-50195748857f)

## Prerequisites

- Python 3.x
- `ping` command available on the Linux PC

## Installation

1. Clone the repository or download the script file: `main.py`.

2. Install the required Python packages by running the following command:
`pip install prometheus_client`

## Usage

1. Run the script using the following command:
`python3 main.py`

2. The script will start a Prometheus server and expose the metrics at `http://localhost:8001`. You can access the Prometheus web interface to view the metrics.

3. The script will continuously send pings to the specified IP address (default: `8.8.8.8`) at regular intervals (default: 1 second). The number of pings sent in each batch can be configured (default: 30).

4. The metrics collected include:

- `ping_latency`: Ping latency statistics (min, avg, max, mdev).
- `packet_loss`: Packet loss percentage.
- `packets_transmitted`: Number of packets transmitted.
- `packets_received`: Number of packets received.

5. The ping output is logged to the `ping.log` file, located in the same directory as the script.

## Customization

- To change the IP address to ping, modify the `ip` variable in the `main` function.

- To adjust the number of pings sent in each batch, modify the `amount_of_pings` variable in the `main` function.

- The Prometheus server port is set to `8001` by default. To change the port, modify the `start_http_server` function call in the `main` function.

## License

This project is licensed under the [MIT License](LICENSE).
