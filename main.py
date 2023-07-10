import subprocess
import re
import os
import time
import logging
from prometheus_client import start_http_server, Gauge

# Get the directory path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Configure logging
logging.basicConfig(filename=os.path.join(script_dir, 'ping.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Prometheus metrics initialization
metrics = {
    'ping_latency': Gauge('ping_latency', 'Ping latency statistics', ['type']),
    'packet_loss': Gauge('packet_loss', 'Packet Loss Percentage'),
    'packets_transmitted': Gauge('packets_transmitted', 'Number of Packets Transmitted'),
    'packets_received': Gauge('packets_received', 'Number of Packets Received')
}

packets_transmitted_count = 0
packets_received_count = 0

def parse_ping_output(output):
    result = re.search(r"(\d+)% packet loss", output)
    packet_loss = int(result.group(1))
    result = re.search(r"(\d+) packets transmitted, (\d+) received", output)
    packets_transmitted = int(result.group(1))
    packets_received = int(result.group(2))
    result = re.search(r"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", output)
    ping_min = float(result.group(1))
    ping_avg = float(result.group(2))
    ping_max = float(result.group(3))
    ping_mdev = float(result.group(4))
    return packet_loss, packets_transmitted, packets_received, ping_min, ping_avg, ping_max, ping_mdev

def update_metrics(packet_loss, ping_min, ping_avg, ping_max, ping_mdev, packets_transmitted, packets_received):
    metrics['ping_latency'].labels('average').set(ping_avg)
    metrics['ping_latency'].labels('minimum').set(ping_min)
    metrics['ping_latency'].labels('maximum').set(ping_max)
    metrics['ping_latency'].labels('mdev').set(ping_mdev)
    metrics['packet_loss'].set(packet_loss)
    metrics['packets_transmitted'].set(packets_transmitted)
    metrics['packets_received'].set(packets_received)

def ping(ip, amount_of_pings):
    global packets_transmitted_count, packets_received_count

    command = f"ping -c {amount_of_pings} {ip}"
    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        packet_loss, packets_transmitted, packets_received, ping_min, ping_avg, ping_max, ping_mdev = parse_ping_output(output)

        # Update the cumulative counts
        packets_transmitted_count += packets_transmitted
        packets_received_count += packets_received

        update_metrics(packet_loss, ping_min, ping_avg, ping_max, ping_mdev, packets_transmitted_count, packets_received_count)
        logging.info(output)  # Log the ping output
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.output}")

def main():
    ip = "8.8.8.8"
    amount_of_pings = 30
    start_http_server(8001)
    while True:
        ping(ip, amount_of_pings)
        time.sleep(1)

if __name__ == "__main__":
    main()
