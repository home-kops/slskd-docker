#!/usr/bin/env python3

import json
import os
import subprocess

logs_dir = os.environ["SLSKD_LOGS_DIR"]
email_address = os.environ["DEST_EMAIL_ADDRESS"]
completed_dir = os.environ["SLSKD_DOWNLOADS_DIR"]
quarantine_dir = os.environ["QUARANTINE_DIR"]
slskd_data = json.loads(os.environ['SLSKD_SCRIPT_DATA'])

directory_to_scan_path = slskd_data['localDirectoryName']
print(f"Directory to scan: {directory_to_scan_path}")

directory_to_scan_name = os.path.basename(directory_to_scan_path)
print(f"Directory to scan name: {directory_to_scan_name}")

log_file = f"{logs_dir}/{directory_to_scan_name}_scan.log"
print(f"Log file: {log_file}")

with open(log_file, "w") as f:
    f.write(f"Scanning directory: {directory_to_scan_path}\n")

subprocess.run(["/bin/sh", "-c", f"clamscan -ir --heuristic-alerts=yes --scan-archive=yes --max-filesize=2000M --max-scansize=2000M \"{directory_to_scan_path}\""], stdout=open(log_file, "a"), stderr=subprocess.STDOUT)

with open(log_file, "r") as f:
    log_contents = f.read()

    if "Infected files: 0" in log_contents:
        message = f"slskd scanned directory {directory_to_scan_name}: No infections found."
        target_dir = completed_dir
    else:
        message = f"Quarantining directory {directory_to_scan_name} due to (potential) infection."
        target_dir = quarantine_dir

    print(message)
    subprocess.run(["/bin/sh", "-c", f"mail -s \"{message}\" \"{email_address}\" < \"{log_file}\""])
    os.rename(directory_to_scan_path, os.path.join(target_dir, directory_to_scan_name))
