# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

This guide shows you how to migrate your Python code from the OpenAI ChatCompletion API to the Azure Inference Chat Completion API. You will learn about parameter mapping, environment setup, and see side-by-side code examples.

## 1. Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 2. Parameter Mapping: OpenAI vs Azure Inference

The following table maps common parameters from the OpenAI `ChatCompletion` API to the Azure Inference `ChatCompletionsClient` API.

| OpenAI Parameter         | Azure Inference Equivalent         | Notes                                                      |
|-------------------------|------------------------------------|------------------------------------------------------------|
| `model`                 | Deployment in endpoint URL         | Azure Inference uses deployment in the endpoint URL         |
| `messages`              | `messages`                         | Both use a list of message objects                         |
| `temperature`           | `temperature`                      | Supported                                                  |
| `max_tokens`            | `max_tokens`                       | Supported                                                  |
| `top_p`                 | `top_p`                            | Supported                                                  |
| `n`                     | `n`                                | Supported                                                  |
| `stop`                  | `stop`                             | Supported                                                  |
| `stream`                | `stream`                           | Supported                                                  |
| `presence_penalty`      | `presence_penalty`                 | Supported                                                  |
| `frequency_penalty`     | `frequency_penalty`                | Supported                                                  |
| `user`                  | Not directly supported             | Not required in Azure Inference                            |
| `api_key`               | `AzureKeyCredential` or Entra ID   | Use AzureKeyCredential or Azure Identity                   |
| `openai.api_base`       | `endpoint`                         | Use full endpoint URL for Azure Inference                  |
| `openai.api_version`    | `api_version`                      | Specify API version for Azure Inference                    |

> **Note:** The message format is similar, but Azure Inference uses specific message classes (`SystemMessage`, `UserMessage`, `AssistantMessage`).

## 3. What You'll Learn

- How to set up your environment for Azure Inference.
- How to translate OpenAI ChatCompletion code to Azure Inference.
- How to run the migrated code.

---

## 4. Environment Setup

### 4.1. Windows

1. **Create and activate a virtual environment:**
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```

2. **Install required libraries:**
    ```cmd
    pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
    ```

3. **Set environment variables:**
    ```cmd
    set AZURE_AI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<deployment-name>
    set AZURE_AI_CHAT_KEY=<your-azure-openai-key>
    ```

### 4.2. Linux/macOS

1. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install required libraries:**
    ```bash
    pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
    ```

3. **Set environment variables:**
    ```bash
    export AZURE_AI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<deployment-name>
    export AZURE_AI_CHAT_KEY=<your-azure-openai-key>
    ```

---

## 5. Code Comparison: OpenAI vs Azure Inference

### 5.1. OpenAI ChatCompletion Example

```python
import openai

openai.api_key = "<your-openai-api-key>"
openai.api_base = "https://api.openai.com/v1"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"}
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message["content"])
```

**Explanation:**
- Sets the API key and base URL.
- Sends a list of messages.
- Receives and prints the assistant's reply.

---

### 5.2. Azure Inference Chat Completion Example

#### Main Components

- **Environment Variables:** Used for endpoint and key.
- **Client Initialization:** Uses `ChatCompletionsClient` and `AzureKeyCredential`.
- **Message Classes:** Uses `SystemMessage` and `UserMessage` for message formatting.
- **Response Handling:** Accesses the assistant's reply from the response.

#### Complete Code Example

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def chat_completion_azure_inference():
    try:
        endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_AI_CHAT_KEY"]
    except KeyError:
        print("Missing AZURE_AI_CHAT_ENDPOINT or AZURE_AI_CHAT_KEY")
        exit(1)

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01"
    )

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?")
    ]

    response = client.complete(
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    chat_completion_azure_inference()
```

---

## 6. How to Run the Example

1. Save the Azure Inference code to a file, for example, `chat_completion_azure.py`.
2. Ensure your environment variables are set as described above.
3. Run the script:
    ```bash
    python chat_completion_azure.py
    ```

---

## 7. Next Steps and Related Resources

- [Azure AI Inference Python SDK Documentation](https://learn.microsoft.com/python/api/overview/azure/ai-inference-readme)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [OpenAI Python Library Documentation](https://platform.openai.com/docs/libraries/python-library)
- [Azure AI Foundry Quickstart](https://learn.microsoft.com/azure/ai-services/foundry/quickstart)

---

By following this guide, you can migrate your OpenAI ChatCompletion code to use Azure Inference with minimal changes, leveraging Azure's security and management features.