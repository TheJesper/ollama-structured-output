import json
import os

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        else:
            # Return a default configuration if the config file is not found
            return {
                "api_endpoint": "http://localhost:11434/api/generate",
                "output_dir": "output",
                "source_dir": "source",
                "test_dir": "test",
                "last_model": "",  # Last model selected by the user
                "save_files": True,  # Option to save or not save files
                "retry_attempts": 3,  # Number of retries for API requests
                "ollama_models_endpoint": "http://localhost:11434/api/models"  # Default models endpoint
            }

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def get_last_model(self):
        return self.config.get("last_model", "")

    def set_last_model(self, model_name):
        """Saves the last selected model."""
        self.config["last_model"] = model_name
        self.save_config()

    def get_api_endpoint(self):
        return self.config.get("api_endpoint", "")

    def get_output_dir(self):
        return self.config.get("output_dir", "")

    def get_source_dir(self):
        return self.config.get("source_dir", "")

    def get_test_dir(self):
        return self.config.get("test_dir", "")

    def should_save_files(self):
        return self.config.get("save_files", True)

    def get_retry_attempts(self):
        return self.config.get("retry_attempts", 3)

    def get_models_endpoint(self):
        return self.config.get("ollama_models_endpoint", "http://localhost:11434/api/models")
