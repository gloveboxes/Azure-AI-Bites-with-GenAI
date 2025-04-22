# 1. Basic Chat Completion with Azure Inference SDK in Python

This guide shows you how to perform a basic chat completion using the Azure Inference SDK in Python. You will set up your environment, install required dependencies, and run a sample script that sends a chat prompt to an Azure AI model and prints the response.

---

## 2. Prerequisites

- Python 3.8 or later installed.
- An Azure AI resource with a deployed chat model.
- Your Azure AI endpoint URL and API key.

---

## 3. What You'll Learn

- How to create a Python virtual environment.
- How to install the Azure Inference SDK and dependencies.
- How to set environment variables for authentication.
- How to use the SDK to send chat messages and receive responses.

---

## 4. Install Dependencies

### 4.1. Create and Activate a Virtual Environment

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4.2. Install Required Packages

```bash
pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
```

---

## 5. Set Environment Variables

Set the following environment variables with your Azure AI endpoint and key.

**Windows (Command Prompt):**
```cmd
set AZURE_AI_CHAT_ENDPOINT=https://<your-endpoint>.openai.azure.com/
set AZURE_AI_CHAT_KEY=<your-api-key>
```

**Linux/macOS (Bash):**
```bash
export AZURE_AI_CHAT_ENDPOINT=https://<your-endpoint>.openai.azure.com/
export AZURE_AI_CHAT_KEY=<your-api-key>
```

Replace `<your-endpoint>` and `<your-api-key>` with your actual values.

---

## 6. Main Code Components Explained

The example code consists of these main components:

| Component                | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Import statements        | Imports required Azure Inference SDK classes and Python modules.             |
| Environment variables    | Reads endpoint and key from environment for authentication.                  |
| Client initialization    | Creates a `ChatCompletionsClient` with endpoint and credentials.            |
| Message construction     | Builds a list of chat messages (system and user) for the model.             |
| Chat completion request  | Sends messages to the model and receives a response.                        |
| Output                   | Prints the model's reply to the console.                                    |

---

## 7. OpenAI to Azure Inference Parameter Mapping

| OpenAI ChatCompletion Parameter | Azure Inference API Parameter |
|---------------------------------|------------------------------|
| `model`                         | Set in Azure deployment      |
| `messages`                      | `messages`                   |
| `temperature`                   | `temperature` (if supported) |
| `max_tokens`                    | `max_tokens` (if supported)  |
| `stop`                          | `stop` (if supported)        |
| `stream`                        | `stream` (if supported)      |

*Note: This example uses only the `messages` parameter for simplicity.*

---

## 8. Complete Example Code

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def basic_chat_completion():
    try:
        endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_AI_CHAT_KEY"]
    except KeyError:
        print("Missing AZURE_AI_CHAT_ENDPOINT or AZURE_AI_CHAT_KEY")
        exit(1)

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("Hello, who won the FIFA World Cup in 2018?")
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    basic_chat_completion()
```

---

## 9. Run the Example

1. Activate your virtual environment if not already active.
2. Ensure your environment variables are set.
3. Run the script:

```bash
python <script-name>.py
```

Replace `<script-name>.py` with the name of your Python file.

---

## 10. Next Steps

- [Azure Inference SDK Documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt)
- [Azure AI Python SDK Reference](https://pypi.org/project/azure-ai-inference/)
- [OpenAI to Azure API Mapping](https://learn.microsoft.com/azure/ai-services/openai/reference#rest-api-versioning)

Explore more advanced features such as conversation history, parameter tuning, and streaming responses.