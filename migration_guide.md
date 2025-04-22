# 1. Basic Chat Completion with Azure Inference SDK in Python

This guide shows you how to perform a basic chat completion using the Azure Inference SDK in Python. You will set up your environment, install required dependencies, and run a sample script that sends a chat prompt to an Azure AI model and prints the response.

---

## 2. Prerequisites

- Python 3.8 or later installed.
- An Azure AI resource with a deployed chat model.
- Your Azure AI resource endpoint and API key.

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

### 4.2. Install Required Python Packages

```bash
pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
```

---

## 5. Set Environment Variables

Set the following environment variables with your Azure AI resource values.

**Windows (Command Prompt):**
```cmd
set AZURE_AI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/
set AZURE_AI_CHAT_KEY=<your-api-key>
```

**Linux/macOS (Bash):**
```bash
export AZURE_AI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/
export AZURE_AI_CHAT_KEY=<your-api-key>
```

Replace `<your-resource-name>` and `<your-api-key>` with your actual values.

---

## 6. OpenAI to Azure Inference Parameter Mapping

| OpenAI ChatCompletion Parameter | Azure Inference API Parameter |
|---------------------------------|------------------------------|
| `messages`                      | `messages`                   |
| `model`                         | Set in Azure deployment      |
| `temperature`                   | `temperature`                |
| `max_tokens`                    | `max_tokens`                 |
| `top_p`                         | `top_p`                      |
| `stop`                          | `stop`                       |

---

## 7. Main Code Components Explained

- **Import libraries:** Import required Azure SDK modules and Python libraries.
- **Read environment variables:** Retrieve endpoint and API key for authentication.
- **Create client:** Initialize `ChatCompletionsClient` with endpoint and credentials.
- **Prepare messages:** Use `SystemMessage` and `UserMessage` to define the chat context and user input.
- **Send request:** Call `client.complete()` with the message list.
- **Print response:** Output the assistant's reply.

---

## 8. Complete Code Example

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
        UserMessage("Hello, can you tell me a fun fact about space?")
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

- [Azure Inference SDK Documentation](https://learn.microsoft.com/azure/ai-services/inference/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Python SDK Reference](https://pypi.org/project/azure-ai-inference/)

Explore adding conversation history, adjusting parameters, or handling errors for more advanced scenarios.