import os
import time
import socket
import psutil
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = os.getenv('API_URL', 'http://localhost:5000/api/v1/stats')
INTERVAL = int(os.getenv('REPORT_INTERVAL', '10'))
# Allow overriding hostname from environment to use the actual host's hostname
HOSTNAME = os.getenv('HOST_HOSTNAME', socket.gethostname())

def get_system_stats():
    """Collect system statistics using psutil."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    # Network usage
    net_io = psutil.net_io_counters()
    network_sent = net_io.bytes_sent
    network_recv = net_io.bytes_recv
    
    return {
        'hostname': HOSTNAME,
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'disk_usage': disk_usage,
        'network_sent': network_sent,
        'network_recv': network_recv
    }

def report_stats(stats):
    """Send collected statistics to the API receiver."""
    try:
        response = requests.post(API_URL, json=stats, timeout=5)
        response.raise_for_status()
        logging.info(f"Reported stats for {stats['hostname']}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to report stats: {e}")

def main():
    logging.info(f"Agent started. Reporting to {API_URL} every {INTERVAL} seconds.")
    while True:
        stats = get_system_stats()
        report_stats(stats)
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
