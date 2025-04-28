# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This guide explains how to migrate your Python code from using the OpenAI ChatCompletion API to the Azure Inference Chat Completion API. You will learn about the required environment setup, the mapping of API parameters, and see side-by-side code examples for both APIs. The goal is to help you transition your chat completion workloads to Azure AI Foundry services with minimal changes.

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
    6. Set up environment variables:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="<your-azure-openai-endpoint>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```
        Replace the placeholders with the actual values for your Azure OpenAI endpoint and key.

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
    6. Set up environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="<your-azure-openai-endpoint>"
        export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```
        Replace the placeholders with the actual values for your Azure OpenAI endpoint and key.

## 2. API Mapping

The following table maps the key parameters between the OpenAI ChatCompletion API and the Azure Inference Chat Completion API.

| OpenAI ChatCompletion Parameter | Azure Inference Chat Completion Parameter | Notes |
|---------------------------------|------------------------------------------|-------|
| `model`                         | Set in endpoint URL (deployment name)    | Azure uses deployment name in the endpoint URL, not as a parameter. |
| `messages`                      | `messages`                               | Both use a list of message objects. |
| `temperature`                   | `temperature`                            | Supported in both APIs. |
| `max_tokens`                    | `max_tokens`                             | Supported in both APIs. |
| `top_p`                         | `top_p`                                  | Supported in both APIs. |
| `n`                             | `n`                                      | Supported in both APIs. |
| `stop`                          | `stop`                                   | Supported in both APIs. |
| `stream`                        | `stream`                                 | Supported in both APIs. |
| `functions`                     | `functions` (as tools)                   | Azure supports function calling as tools. |
| `response_format`               | `response_format`                        | Supported in both APIs. |
| `api_key`                       | `AZURE_OPENAI_CHAT_KEY` (env variable)   | Azure uses environment variable or AzureKeyCredential. |
| `api_base`                      | `AZURE_OPENAI_CHAT_ENDPOINT` (env variable) | Azure uses environment variable for endpoint. |
| `api_version`                   | `api_version`                            | Required in Azure client. |

## 3. Main code components

### 3.1 OpenAI ChatCompletion Example

This code demonstrates how to use the OpenAI ChatCompletion API to get a chat response.

**Explanation:**  
You create a client using your OpenAI API key, specify the model, and send a list of messages. The response contains the assistant's reply.

```python
import openai

openai.api_key = "<your-openai-api-key>"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"},
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message["content"])
```

### 3.2 Azure Inference Chat Completion Example

This code demonstrates how to use the Azure Inference Chat Completion API to get a chat response.

**Explanation:**  
You create a `ChatCompletionsClient` using your Azure OpenAI endpoint and key, then send a list of messages. The response contains the assistant's reply.

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
    max_tokens=100,
)

print(response.choices[0].message.content)
```

## 4. Complete code

The following is the complete Azure Inference Chat Completion example. Save this code as `example.py`.

**Explanation:**  
This script loads the required environment variables, creates a client, sends a chat completion request, and prints the assistant's response.

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
        api_version="2024-06-01",
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ],
        temperature=0.7,
        max_tokens=100,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

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
- [OpenAI Python API reference](https://platform.openai.com/docs/api-reference/chat/create){:target="_blank"}
- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}