import requests
from halo import Halo
import json
import os
from pydantic import ValidationError, create_model
from file_handler import save_response, compare_responses
from deepdiff import DeepDiff
import subprocess

def create_pydantic_model_from_schema(schema):
    fields = {
        key: (str if value["type"] == "string" else int, ...)
        for key, value in schema["properties"].items()
    }
    model = create_model(schema["title"], **fields)
    return model

def validate_response(schema, response_data):
    model = create_pydantic_model_from_schema(schema)
    try:
        validated_data = model(**response_data)
        return validated_data.dict(), None
    except ValidationError as e:
        return None, str(e)

def interact_with_model(config_manager, model_name, schema, context):
    api_endpoint = config_manager.get_api_endpoint()

    with open(os.path.join(config_manager.get_source_dir(), "prompt.txt"), "r") as prompt_file:
        prompt_text = prompt_file.read().strip()

    full_prompt = f"{prompt_text}\n\nSchema:\n{json.dumps(schema, indent=2)}\n\nContext:\n{context}"

    spinner = Halo(text=f'Interacting with {model_name}...', spinner='dots')
    spinner.start()

    response = requests.post(api_endpoint, json={
        "model": model_name,
        "prompt": full_prompt,
        "format": "json",
        "stream": False
    })

    spinner.stop()

    if response.status_code == 200:
        return json.loads(response.json().get("response", "{}"))
    else:
        print("❌ API Error: ", response.status_code)
        return None

def interact_with_model_with_retries(config_manager, model_name, schema, context):
    retries = config_manager.get_retry_attempts()
    for attempt in range(retries + 1):
        attempt_text = "Initial" if attempt == 0 else f"Retry {attempt}"
        print(f"\nAttempt {attempt + 1} ({attempt_text})")
        response = interact_with_model(config_manager, model_name, schema, context)
        if response:
            validated_response, error = validate_response(schema, response)
            if not error:
                return validated_response, attempt
        print(f"❌ Validation Error on attempt {attempt + 1}: {error}")
    return None, retries

def list_models(config_manager):
    """List all available models installed with Ollama."""
    base_url = config_manager.get_api_endpoint().split('/api')[0]
    api_endpoint = f"{base_url}/v1/models"
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        models_data = response.json().get("data", [])
        models = [model['id'] for model in models_data]
        return models
    else:
        print(f"❌ API Error: {response.status_code}")
        return []

def run_ollama_test(config_manager, model_name, schema, context, num_rounds=10):
    runtimes = []

    for i in range(num_rounds):
        spinner = Halo(text=f'Running test round {i+1}/{num_rounds} for {model_name}...', spinner='dots')
        spinner.start()
        
        response = interact_with_model(config_manager, model_name, schema, context)
        runtimes.append(response.get('total_duration', 0))
        
        spinner.stop()

    return runtimes

def download_model(config_manager, model_name):
    api_endpoint = config_manager.get_api_endpoint().replace("/generate", "/pull")
    payload = {"name": model_name}

    spinner = Halo(text=f"Downloading model '{model_name}'...", spinner='dots')
    spinner.start()

    response = requests.post(api_endpoint, json=payload)
    spinner.stop()

    if response.status_code == 200:
        # Verify if the model was successfully downloaded by listing models again
        models = list_models(config_manager)
        if model_name in models:
            return True
        else:
            print(f"\n❌ Error: Model '{model_name}' was not found after download. It may not exist.")
            return False
    else:
        print(f"\n❌ API Error: {response.status_code} - {response.text}")
        return False