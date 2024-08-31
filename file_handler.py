import os
import json
from deepdiff import DeepDiff
from datetime import datetime

def save_response(config_manager, response, response_only=True):
    if not config_manager.should_save_files():
        return

    output_dir = config_manager.get_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp if 'created_at' is not available in response
    timestamp = response.get('created_at', datetime.now().isoformat().replace(":", "-"))

    if response_only:
        response_only_file = os.path.join(output_dir, f"{timestamp}_response_only.json")
        with open(response_only_file, "w") as file:
            json.dump(response, file, indent=2)
    else:
        raw_response_file = os.path.join(output_dir, f"{timestamp}_raw_response.json")
        with open(raw_response_file, "w") as file:
            json.dump(response, file, indent=2)

def load_test_files(config_manager):
    schema_file_path = os.path.join(config_manager.get_test_dir(), "schema.json")
    context_file_path = os.path.join(config_manager.get_test_dir(), "context.txt")
    expected_response_path = os.path.join(config_manager.get_test_dir(), "expected_unicorn_land.json")

    with open(schema_file_path, "r") as schema_file, open(context_file_path, "r") as context_file, open(expected_response_path, "r") as expected_file:
        schema = json.load(schema_file)
        context = context_file.read().strip()
        expected_response = json.load(expected_file)

    return schema, context, expected_response

def compare_responses(expected, actual):
    diff = DeepDiff(expected, actual, ignore_order=True)
    return diff == {}

def clear_saved_files(config_manager):
    output_dir = config_manager.get_output_dir()
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        print("All saved files cleared.")
    else:
        print("No saved files found to clear.")
