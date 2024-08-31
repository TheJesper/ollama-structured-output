import requests
import json
import os
from pydantic import ValidationError, create_model

# Function to load the schema from a file
def load_schema(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path and try again.")
        exit(1)

# Function to map JSON schema types to Python types
def map_json_type(json_type):
    if json_type == "string":
        return str
    elif json_type == "integer":
        return int
    else:
        raise ValueError(f"Unsupported JSON schema type: {json_type}")

# Function to create a Pydantic model from a JSON schema
def create_pydantic_model(schema):
    model_name = schema.get('title', 'GeneratedModel')
    fields = {
        key: (map_json_type(value["type"]), ...)
        for key, value in schema['properties'].items()
    }
    return create_model(model_name, **fields)

# Function to validate and print the response
def validate_and_print_response(response, model):
    try:
        validated_data = model(**json.loads(response["response"]))
        print("\nValidated Response:\n", json.dumps(validated_data.dict(), indent=2))
    except ValidationError as e:
        print(f"Validation Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

# Convert schema to a string representation
def convert_schema_to_string(schema):
    schema_string = "{\n"
    for key, value in schema['properties'].items():
        schema_string += f'  "{key}": "{value["type"]} - {value["description"]}",\n'
    schema_string += "}"
    return schema_string

# Main function to load schema, send API request, and validate the response
def main():
    schema_file_path = os.path.join("source", "schema.json")
    schema = load_schema(schema_file_path)
    
    CountryDetails = create_pydantic_model(schema)

    # Read the context and prompt
    with open(os.path.join("source", "context.txt"), "r") as file:
        context = file.read()
    
    with open(os.path.join("source", "prompt.txt"), "r") as file:
        prompt = file.read()

    # Convert schema to string and append to the prompt
    schema_string = convert_schema_to_string(schema)
    full_prompt = f"{prompt}\n\n{context}\n\nPlease respond with the following structure:\n{schema_string}"

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": full_prompt,
        "format": "json",
        "stream": False
    }).json()

    # Save raw response
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"raw_response_{response['created_at'].replace(':', '-')}.json")
    with open(output_file, "w") as file:
        json.dump(response, file, indent=2)

    # Save only the extracted response part
    response_only_file = os.path.join(output_dir, f"response_only_{response['created_at'].replace(':', '-')}.json")
    with open(response_only_file, "w") as file:
        json.dump(json.loads(response["response"]), file, indent=2)

    # Validate and print the response
    validate_and_print_response(response, CountryDetails)

if __name__ == "__main__":
    main()
