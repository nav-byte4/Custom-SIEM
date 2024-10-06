import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
import os

# Log parsing function
def parse_log(log_entry):
    pattern = r'(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d{3}) (\d+)'
    match = re.match(pattern, log_entry)
    if match:
        log_data = {
            'ip': match.group(1),
            'timestamp': match.group(4),
            'request': match.group(5),
            'status_code': match.group(6),
            'response_size': match.group(7)
        }
        return log_data
    else:
        return None

# Failed login monitoring
failed_logins = defaultdict(list)
ALERT_THRESHOLD = 5  # Threshold for failed login attempts

def check_failed_login(ip, timestamp):
    failed_logins[ip].append(timestamp)
    failed_logins[ip] = [t for t in failed_logins[ip] if t > datetime.now() - timedelta(minutes=5)]
    
    if len(failed_logins[ip]) >= ALERT_THRESHOLD:
        send_alert(ip)

# Send alert when threshold is met
def send_alert(ip):
    print(f"ALERT! Multiple failed login attempts from {ip}")
    block_ip(ip)

# Block IP function (optional, if you want to block an IP)
def block_ip(ip):
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
    print(f"Blocked IP: {ip}")

# Main script
def main():
    # Simulate failed logins from an IP (use your actual IP or a test IP)
    ip_address = '192.168.1.100'  # Replace this with a real or test IP

    # Simulate 5 failed login attempts within 5 minutes
    for _ in range(5):
        log_entry = f'{ip_address} - - [10/Oct/2024:13:55:36 +0000] "GET /login" 401 2326'
        parsed_log = parse_log(log_entry)
        if parsed_log:
            check_failed_login(parsed_log['ip'], datetime.now())

    
   

if __name__ == '__main__':
    main()
