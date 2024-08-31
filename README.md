
# Ollama Structured Output 🛠️

Welcome to **Ollama Structured Output** – a powerful tool designed to help you interact with models via the Ollama API, extract structured responses, and validate them against predefined schemas. Developed with the assistance of both AI and human input, this tool is perfect for developers and data scientists who need efficient and reliable structured data extraction.

## 🚀 Features

- **Normal Run**: Run the tool using your source folder files to interact with the model and extract structured responses.
- **Test Mode**: Run multiple iterations of tests using predefined contexts, prompts, and schemas. Analyze efficiency, retry attempts, and validation success rates.
- **Model Management**: List all available models, select models, and download new models directly through the tool.
- **Data Logging**: Logs test results with detailed metrics like successful runs, failed runs, retries, and efficiency.
- **File Management**: Clear saved output files and test results effortlessly.

## 🛠️ Usage

1. **Normal Run**: 
   - Runs the tool using the context and schema in the source folder to interact with the selected model.

2. **Test Run**: 
   - Specify the number of iterations to test the tool. The tool runs the context and schema in the test folder and provides a detailed report on performance.

3. **Model Selection**: 
   - List all available models and select one to be used for subsequent runs.

4. **Download Models**: 
   - Download a new model by entering its name or selecting from a list of available models.

5. **View Test Results**: 
   - Displays a compact summary of recent test results, including key metrics.

6. **Clear Data**: 
   - Options to clear saved output files and test results, keeping your workspace clean.

## 📋 Requirements

- **Python 3.8+**
- **pip** (to install required packages)
- **Ollama API** configured and running locally.

## 🧩 Installation

Clone the repository and navigate to the project directory:

```
git clone https://github.com/TheJesper/ollama-structured-output.git
cd ollama-structured-output
```

Install the required Python packages:

```
pip install -r requirements.txt
```

Make sure you have the **Ollama API** running locally. Adjust the configuration in `config.json` if necessary.

## ⚙️ Configuration

The configuration file `config/config.json` allows you to customize various aspects of the tool, including the API endpoint, directories for source and test files, and options for saving files. 

### Example `config.json`:

```
{
  "api_endpoint": "http://localhost:11434/api/generate",
  "output_dir": "output",
  "source_dir": "source",
  "test_dir": "test",
  "last_model": "gemma2:latest",
  "save_files": true,
  "retry_attempts": 3
}
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

- **Jesper Wilfing**
- **Comzeon AB, Gothenburg, Sweden**

Contributions are welcome! Feel free to fork this repository and submit pull requests.

---

*Developed with the help of AI and human collaboration.* 🤖🤝
