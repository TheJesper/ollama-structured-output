import json
import os
import time
from api_handler import interact_with_model_with_retries
from file_handler import compare_responses, load_test_files
from test_logger import log_test_results
from tabulate import tabulate

def run_test_iterations(config_manager, iterations):
    schema, context, expected_response = load_test_files(config_manager)

    successful_runs = 0
    failed_runs = 0
    total_retries = 0
    start_time = time.time()

    for i in range(iterations):
        print(f"\nTest Iteration {i + 1}/{iterations}")
        
        validated_response, retries = interact_with_model_with_retries(config_manager, config_manager.get_last_model(), schema, context)
        retries_counted = retries - 1
        total_retries += max(0, retries_counted)

        if compare_responses(expected_response, validated_response):
            successful_runs += 1
            print("✅ Response matched expected output.")
        else:
            failed_runs += 1
            print("❌ Response did not match expected output.")

        print(f"\nResponse:\n{json.dumps(validated_response, indent=2)}")

    total_time = time.time() - start_time

    test_data = {
        "number_of_runs": iterations,
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "total_retries": total_retries,
        "time_taken_seconds": round(total_time, 2),
        "efficiency": calculate_efficiency(successful_runs, total_retries, total_time),
        "model": config_manager.get_last_model()
    }

    log_test_results(test_data)

    print("\n🧠 Test Summary 🛠️")
    summary_table = [
        ["Number of Runs", iterations],
        ["Successful Runs", successful_runs],
        ["Failed Runs", failed_runs],
        ["Total Retries", total_retries],
        ["Time Taken (seconds)", round(total_time, 2)],
        ["Efficiency", calculate_efficiency(successful_runs, total_retries, total_time)]
    ]
    print(tabulate(summary_table, headers=["Metric", "Value"], tablefmt="grid"))

def clear_test_log():
    log_file_path = os.path.join("test_logs", "test_log.json")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        print("Test log cleared.")
    else:
        print("No test log found to clear.")

def calculate_efficiency(successful_runs, total_retries, total_time):
    if successful_runs == 0:
        return -total_retries
    return (successful_runs / total_time) - (total_retries / successful_runs)
