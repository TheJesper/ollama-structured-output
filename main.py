import json
import os
from config_manager import ConfigManager
from api_handler import interact_with_model_with_retries, list_models, download_model
from file_handler import save_response, clear_saved_files
from test_handler import run_test_iterations, clear_test_log
from test_logger import load_test_log
from tabulate import tabulate

def display_test_results():
    test_log = load_test_log()
    if not test_log:
        print("\nNo test results found.")
        return

    print("\n📊 Test Results Log 🛠️")
    
    # Legend
    legend = {
        "Number of Runs": "🏃",
        "Model": "🧠",
        "Successful Runs": "✅",
        "Failed Runs": "❌",
        "Total Retries": "🔄",
        "Time Taken (seconds)": "⏱️",
        "Efficiency": "⚡"
    }
    print("Legend:")
    for k, v in legend.items():
        print(f"{v}: {k}")

    # Slim table using emojis
    slim_log = [
        {legend["Number of Runs"]: log["number_of_runs"],
         legend["Model"]: log["model"],
         legend["Successful Runs"]: log["successful_runs"],
         legend["Failed Runs"]: log["failed_runs"],
         legend["Total Retries"]: log["total_retries"],
         legend["Time Taken (seconds)"]: log["time_taken_seconds"],
         legend["Efficiency"]: log["efficiency"]}
        for log in test_log
    ]
    print("\nTest Results:")
    print(tabulate(slim_log, headers="keys", tablefmt="grid"))

def main():
    config_path = os.path.join("config", "config.json")
    config_manager = ConfigManager(config_path)

    selected_model = config_manager.get_last_model()

    while True:
        print(f"\n🧠  Ollama Structured Output Tool 🛠️")
        print(f"Selected Model: {selected_model}\n")
        print("1.▶️  Normal run from source folder")
        print("2.🧪 Test run from test folder with multiple iterations")
        print("3.🤖 List all models and select")
        print("4.📥 Download and select new model")
        print("5.📊 Show test results")
        print("6.🗑️  Clear test results")
        print("7.🧹 Clear saved output files")
        print("8.🚪 Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            schema_file_path = os.path.join(config_manager.get_source_dir(), "schema.json")
            context_file_path = os.path.join(config_manager.get_source_dir(), "context.txt")
            with open(schema_file_path, "r") as schema_file, open(context_file_path, "r") as context_file:
                schema = json.load(schema_file)
                context = context_file.read().strip()

            validated_response, retries = interact_with_model_with_retries(config_manager, selected_model, schema, context)
            if validated_response:
                print("\nValidated Response:\n", json.dumps(validated_response, indent=2))
                save_response(config_manager, validated_response, response_only=True)

        elif choice == '2':
            iterations = int(input("Enter the number of test iterations: "))
            run_test_iterations(config_manager, iterations)

        elif choice == '3':
            models = list_models(config_manager)
            if models:
                print("\nAvailable Models:\n")
                for idx, model in enumerate(models, 1):
                    print(f"{idx}. {model}")
                model_choice = int(input("\nSelect a model by number: "))
                selected_model = models[model_choice - 1]
                config_manager.set_last_model(selected_model)
                print(f"\nSelected Model: {selected_model}")
            else:
                print("\nNo models found.")

        elif choice == '4':
            model_name = input("Enter the model name to download (e.g., llama3): ")
            download_successful = download_model(config_manager, model_name)
            if download_successful:
                selected_model = model_name
                config_manager.set_last_model(selected_model)
                print(f"\nModel '{model_name}' downloaded and selected.")
            else:
                print(f"\n❌ Error: Model '{model_name}' was not found after download. It may not exist.")

        elif choice == '5':
            display_test_results()

        elif choice == '6':
            confirm = input("Are you sure you want to clear all test results? (y/n): ")
            if confirm.lower() == 'y' or confirm == '':
                clear_test_log()
                print("Test results cleared.")

        elif choice == '7':
            confirm = input("Are you sure you want to clear all saved output files? (y/n): ")
            if confirm.lower() == 'y' or confirm == '':
                clear_saved_files(config_manager)
                print("Saved output files cleared.")

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("\n❌ Invalid choice, please try again.")

if __name__ == "__main__":
    main()
