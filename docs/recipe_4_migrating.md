# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This guide explains how to migrate your code from the OpenAI `ChatCompletion` API to the Azure Inference Chat Completion API. You will learn about the required environment setup, the mapping of API parameters, and see code examples for both APIs. The goal is to help you transition your chat completion workloads to Azure AI Foundry services with minimal changes.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a new project folder:
        ```powershell
        mkdir azure-inference-migration
        cd azure-inference-migration
        ```
    3. Set up a virtual environment:
        ```powershell
        python -m venv .venv
        ```
    4. Activate the virtual environment:
        ```powershell
        .\.venv\Scripts\Activate
        ```
    5. Install the required libraries:
        ```powershell
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a new project folder:
        ```bash
        mkdir azure-inference-migration
        cd azure-inference-migration
        ```
    3. Set up a virtual environment:
        ```bash
        python3 -m venv .venv
        ```
    4. Activate the virtual environment:
        ```bash
        source .venv/bin/activate
        ```
    5. Install the required libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

## 2. API Mapping

The following table maps the parameters between the OpenAI `ChatCompletion` API and the Azure Inference Chat Completion API.

| OpenAI `ChatCompletion.create` | Azure Inference `ChatCompletionsClient.complete` | Notes |
|-------------------------------|--------------------------------------------------|-------|
| `model`                       | Deployment is specified in the endpoint URL      | Azure uses deployment in the endpoint, not as a parameter |
| `messages`                    | `messages`                                       | Both use a list of message objects |
| `temperature`                 | `temperature`                                    | Supported in both |
| `max_tokens`                  | `max_tokens`                                     | Supported in both |
| `top_p`                       | `top_p`                                          | Supported in both |
| `n`                           | `n`                                              | Supported in both |
| `stop`                        | `stop`                                           | Supported in both |
| `stream`                      | `stream`                                         | Supported in both |
| `presence_penalty`            | `presence_penalty`                               | Supported in both |
| `frequency_penalty`           | `frequency_penalty`                              | Supported in both |
| `logit_bias`                  | `logit_bias`                                     | Supported in both |
| `user`                        | `user`                                           | Supported in both |
| `api_key`                     | `credential=AzureKeyCredential(key)`             | Azure uses `AzureKeyCredential` |
| `api_base`                    | `endpoint`                                       | Azure uses `endpoint` |
| `api_version`                 | `api_version`                                    | Azure requires explicit API version |

## 3. Main code components

### 3.1 OpenAI Chat Completion Example

This example demonstrates how to use the OpenAI `openai` library to get a chat completion.

```python
import openai

openai.api_key = "<your-openai-api-key>"

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
This code sends a chat completion request to the OpenAI API using the `openai` library. It specifies the model, messages, and other parameters, and prints the assistant's reply.

### 3.2 Azure Inference Chat Completion Example

This example demonstrates how to use the Azure Inference SDK to get a chat completion.

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
    api_version="2024-06-01"
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?")
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message.content)
```

**Explanation:**  
This code uses the Azure Inference SDK to send a chat completion request. The endpoint and key are read from environment variables. The message objects are created using the Azure SDK's `SystemMessage` and `UserMessage` classes.

## 4. Complete code example

The following is a complete example for Azure Inference Chat Completion. Save this code as `example.py`.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    try:
        endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_OPENAI_CHAT_KEY"]
    except KeyError:
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT' or 'AZURE_OPENAI_CHAT_KEY'")
        print("Set them before running this sample.")
        exit()

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01"
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?")
        ],
        temperature=0.7,
        max_tokens=100
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script initializes the Azure Inference client, sends a chat completion request, and prints the response. It uses environment variables for configuration.

## 5. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the code as `example.py`.
3. Run the script:

    ```bash
    python example.py
    ```

## 6. Next steps

- [Azure AI Inference Python SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}
- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure AI Foundry developer guides](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}