import subprocess
import time
import os
from datetime import datetime

# File to store WiFi connection logs
LOG_FILE = "wifi_log.txt"
CHECK_INTERVAL = 10  # Time (in seconds) to wait between checks

def get_connected_ssid():
    """
    Checks the currently connected WiFi SSID.
    Supports Windows and macOS.
    """
    try:
        # For Windows
        if os.name == 'nt':
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], encoding="utf-8"
            )
            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        
        # For macOS
        elif os.name == 'posix':
            output = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                encoding="utf-8"
            )
            for line in output.split("\n"):
                if " SSID:" in line:
                    return line.split(":")[1].strip()

    except subprocess.CalledProcessError as e:
        print(f"Error fetching WiFi SSID: {e}")
    return None

def log_wifi(ssid):
    """
    Logs the current SSID along with the timestamp to a file.
    """
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - Connected to: {ssid}\n")
        print(f"{timestamp} - Logged WiFi: {ssid}")

def main():
    """
    Main loop to continually check and log the WiFi connection.
    """
    last_ssid = None
    
    print("Starting WiFi Logger...")
    while True:
        ssid = get_connected_ssid()
        if ssid and ssid != last_ssid:
            log_wifi(ssid)
            last_ssid = ssid
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
