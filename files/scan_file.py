#!/usr/bin/env python

import json
import os
import subprocess

logs_dir = "./log"
email_address = os.environ["DEST_EMAIL_ADDRESS"]
completed_dir = os.environ["SLSKD_DOWNLOADS_DIR"]
quarantine_dir = os.environ["QUARANTINE_DIR"]
slskd_data = json.loads(os.environ['SLSKD_SCRIPT_DATA'])

file_to_scan_path = slskd_data['localDirectoryName']
print(f"File to scan: {file_to_scan_path}")

file_to_scan_name = os.path.basename(file_to_scan_path)
print(f"File to scan name: {file_to_scan_name}")

log_file = f"{logs_dir}/{file_to_scan_name}_scan.log"
print(f"Log file: {log_file}")

with open(log_file, "w") as f:
    f.write(f"Scanning file: {file_to_scan_path}\n")

subprocess.run(["/bin/sh", "-c", f"clamscan -ir --heuristic-alerts=yes --scan-archive=yes --max-filesize=2000M --max-scansize=2000M {file_to_scan_path}"], stdout=open(log_file, "a"), stderr=subprocess.STDOUT)

with open(log_file, "r") as f:
    log_contents = f.read()

    if "Infected files: 0" in log_contents:
        message = f"slskd scanned file {file_to_scan_name}: No infections found."
        target_dir = completed_dir
    else:
        message = f"Quarantining file {file_to_scan_name} due to (potential) infection."
        target_dir = quarantine_dir

    print(message)
    subprocess.run(["/bin/sh", "-c", f"mail -s \"{message}\" \"{email_address}\" < \"{log_file}\""])
    os.rename(file_to_scan_path, os.path.join(target_dir, file_to_scan_name))
