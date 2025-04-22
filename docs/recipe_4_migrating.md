# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

This guide shows you how to migrate your code from the OpenAI ChatCompletion API to the Azure Inference Chat Completion API. It includes a parameter mapping table and code examples for both APIs.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Parameter Mapping: OpenAI vs Azure Inference

| OpenAI ChatCompletion Parameter | Azure Inference Equivalent         | Notes                                                                 |
|---------------------------------|------------------------------------|-----------------------------------------------------------------------|
| `model`                         | Set in endpoint URL                | Azure Inference uses deployment name in the endpoint URL              |
| `messages`                      | `messages`                         | Both use a list of message objects                                    |
| `temperature`                   | `temperature`                      | Same parameter                                                        |
| `top_p`                         | `top_p`                            | Same parameter                                                        |
| `max_tokens`                    | `max_tokens`                       | Same parameter                                                        |
| `stop`                          | `stop`                             | Same parameter                                                        |
| `n`                             | `n`                                | Same parameter                                                        |
| `stream`                        | `stream`                           | Same parameter                                                        |
| `presence_penalty`              | `presence_penalty`                 | Same parameter                                                        |
| `frequency_penalty`             | `frequency_penalty`                | Same parameter                                                        |
| `logit_bias`                    | `logit_bias`                       | Same parameter                                                        |
| `user`                          | `user`                             | Same parameter                                                        |
| `api_key`                       | `AzureKeyCredential` or Entra ID   | Use AzureKeyCredential or Azure Identity for authentication           |
| `openai.api_base`               | `endpoint`                         | Azure endpoint includes deployment name                               |
| `openai.api_version`            | `api_version`                      | Specify Azure OpenAI API version                                      |

> **Note:** The message format is similar, but Azure Inference uses `SystemMessage`, `UserMessage`, and `AssistantMessage` classes.

## 2. Environment Setup

Follow these steps to set up your environment for Azure Inference.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install required libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
        set AZURE_OPENAI_CHAT_KEY=<your-key>
        ```

=== "Linux/macOS"
    1. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    2. Install required libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
        export AZURE_OPENAI_CHAT_KEY=<your-key>
        ```

## 3. Main Code Components

### 3.1 OpenAI ChatCompletion Example

**Explanation:**  
This example uses the OpenAI Python SDK to get a chat completion.

```python
import openai

openai.api_key = "<your-openai-api-key>"
openai.api_base = "https://api.openai.com/v1"
openai.api_version = None  # Not required for OpenAI public API

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"},
    ],
    temperature=0.7,
    max_tokens=50,
)

print(response.choices[0].message["content"])
```

### 3.2 Azure Inference Chat Completion Example

**Explanation:**  
This example uses the Azure Inference SDK to get a chat completion. It uses environment variables for endpoint and key.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",
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
```

## 4. Complete Example: Azure Inference Chat Completion

**Explanation:**  
This script demonstrates a full migration from OpenAI to Azure Inference, using environment variables for configuration.

```python
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
        api_version="2024-06-01",
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

## 5. How to Run the Example

1. Set up your environment as described above.
2. Save the Azure Inference example code to a file, for example, `azure_inference_chat.py`.
3. Run the script:
    ```bash
    python azure_inference_chat.py
    ```

## 6. Next Steps

- Learn more about [Azure AI Inference SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- Review [Azure OpenAI API documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}
- Explore [OpenAI to Azure OpenAI migration guidance](https://learn.microsoft.com/azure/ai-services/openai/migration){:target="_blank"}