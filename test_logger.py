import json
import os
from datetime import datetime

def log_test_results(test_data):
    log_file_path = os.path.join("test_logs", "test_log.json")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    test_data['timestamp'] = datetime.now().isoformat()

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            log_entries = json.load(log_file)
    else:
        log_entries = []

    log_entries.append(test_data)

    with open(log_file_path, "w") as log_file:
        json.dump(log_entries, log_file, indent=2)

def load_test_log():
    log_file_path = os.path.join("test_logs", "test_log.json")
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            return json.load(log_file)
    else:
        return []

def clear_test_log():
    log_file_path = os.path.join("test_logs", "test_log.json")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        print("Test log cleared.")
    else:
        print("No test log found to clear.")
