# Migrate from OpenAI Chat Completion to Azure OpenAI Chat Completion API

This guide shows you how to migrate your Python code from the OpenAI Chat Completion API to the Azure OpenAI Chat Completion API using key authentication. You will learn about parameter mapping, see code examples for both APIs, and understand the key differences.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services and an Azure OpenAI deployment
- API key for your Azure OpenAI resource

---

## 1. Parameter Mapping: OpenAI vs Azure OpenAI Chat Completion

| OpenAI Parameter         | Azure OpenAI Parameter         | Notes                                                                                 |
|------------------------- |-------------------------------|---------------------------------------------------------------------------------------|
| `model`                  | Deployment in endpoint URL     | Azure uses deployment name in the endpoint URL, not as a parameter                    |
| `messages`               | `messages`                     | Same structure: list of message objects                                               |
| `temperature`            | `temperature`                  | Same                                                                                  |
| `max_tokens`             | `max_tokens`                   | Same                                                                                  |
| `top_p`                  | `top_p`                        | Same                                                                                  |
| `stop`                   | `stop`                         | Same                                                                                  |
| `api_key` (in header)    | `AzureKeyCredential`           | Passed as credential in Azure SDK                                                     |
| `openai.api_base`        | `endpoint`                     | Azure endpoint includes deployment name                                               |
| `openai.ChatCompletion.create()` | `ChatCompletionsClient.complete()` | Different method names and SDKs                                                      |

---

## 2. Install Dependencies

Create a virtual environment and install the required libraries.

```bash
python -m venv .venv
# Activate the environment:
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install openai==1.30.5 azure-ai-inference==1.0.0b9 azure-core==1.33.0
```

---

## 3. Set Environment Variables

Set the following environment variables before running the Azure OpenAI example:

- `AZURE_OPENAI_CHAT_ENDPOINT`  
  Example: `https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>`
- `AZURE_OPENAI_CHAT_KEY`  
  Your Azure OpenAI API key

On Windows (Command Prompt):

```cmd
set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
set AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
```

On Linux/macOS (Bash):

```bash
export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
export AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
```

---

## 4. Code Example: OpenAI Chat Completion

```python
# openai_chat_completion_example.py

import openai

openai.api_key = "<your-openai-api-key>"
openai.api_base = "https://api.openai.com/v1"

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"},
    ],
    temperature=0.7,
    max_tokens=50,
)

print(response.choices[0].message.content)
```

---

## 5. Code Example: Azure OpenAI Chat Completion (Key Authentication)

```python
# azure_openai_chat_completion_example.py

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_OPENAI_CHAT_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01",  # Use the latest supported API version
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ],
        temperature=0.7,
        max_tokens=50,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

---

## 6. How to Run the Example Code

1. Activate your virtual environment.
2. Set the required environment variables for Azure OpenAI.
3. Run the script:

```bash
python azure_openai_chat_completion_example.py
```

---

## 7. Next Steps and Related Resources

- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Inference SDK documentation](https://learn.microsoft.com/python/api/overview/azure/ai-inference-readme)
- [OpenAI Python Library documentation](https://platform.openai.com/docs/libraries/python-library)
- [Azure OpenAI API reference](https://learn.microsoft.com/azure/ai-services/openai/reference)

---

By following this guide, you can migrate your chat completion code from OpenAI to Azure OpenAI with minimal changes, while taking advantage of Azure's deployment and security features.