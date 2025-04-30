# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This article explains how to migrate your code from using the OpenAI Chat Completion API to the Azure AI Inference Chat Completion API. You will learn about the differences in API parameters, authentication, and see side-by-side code examples to help you update your applications.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Foundry provides secure access to AI models and services. You can authenticate using an API key for the Azure Inference SDK.

To authenticate:

1. Go to the Azure AI Foundry portal.
2. Select your model deployment.
3. From the **SDK** dropdown, select **Azure Inference SDK**.
4. Choose **Authentication type** as **Key Authentication**.
5. Copy the **Key** and **Endpoint** values for use in your application.

## 2. Developer environment setup

Select your preferred operating system and follow the steps below.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
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
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_INFERENCE_ENDPOINT = "<your-endpoint>"
        $env:AZURE_INFERENCE_KEY = "<your-key>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
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
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_INFERENCE_ENDPOINT="<your-endpoint>"
        export AZURE_INFERENCE_KEY="<your-key>"
        ```

## 3. API Mapping

The following table maps the parameters between the OpenAI ChatCompletion API and the Azure Inference Chat Completion API.

| OpenAI ChatCompletion Parameter | Azure Inference Chat Completion Parameter | Notes |
|---------------------------------|------------------------------------------|-------|
| `model`                        | Set in deployment endpoint or `model`    | Azure Inference uses the endpoint to specify the model. |
| `messages`                     | `messages`                               | Both use a list of message objects. |
| `temperature`                  | `temperature`                            | Same meaning. |
| `max_tokens`                   | `max_tokens`                             | Same meaning. |
| `top_p`                        | `top_p`                                  | Same meaning. |
| `n`                            | `n`                                      | Same meaning. |
| `stop`                         | `stop`                                   | Same meaning. |
| `stream`                       | `stream`                                 | Same meaning. |
| `presence_penalty`             | `presence_penalty`                       | Same meaning. |
| `frequency_penalty`            | `frequency_penalty`                      | Same meaning. |
| `logit_bias`                   | `logit_bias`                             | Same meaning. |
| `user`                         | `user`                                   | Same meaning. |
| `functions`                    | `tools`                                  | Azure Inference uses `tools` for function calling. |
| `function_call`                | `tool_choice`                            | Azure Inference uses `tool_choice` for tool selection. |
| `response_format`              | `response_format`                        | Both support structured output. |
| `api_key`                      | `credential=AzureKeyCredential(key)`     | Azure Inference uses AzureKeyCredential. |
| `base_url`                     | `endpoint`                               | Azure Inference uses the full endpoint URL. |

## 4. Main code components

### 4.1 OpenAI Chat Completion Example

This example shows how to use the OpenAI ChatCompletion API to get a chat completion.

```python
"""
Get a chat completion using OpenAI's API.
"""

import os

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

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

### 4.2 Azure Inference Chat Completion Example

This example shows how to use the Azure AI Inference client library to get a chat completion.

```python
"""
Get a chat completion using Azure AI Inference.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
key = os.environ["AZURE_INFERENCE_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    temperature=0.7,
    max_tokens=100,
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)

print(response.choices[0].message.content)
```

## 5. Complete code

The following is a complete example for Azure Inference. Save this as `example.py`.

```python
"""
example.py

Get a chat completion using Azure AI Inference.

This script demonstrates how to migrate from OpenAI ChatCompletion to Azure Inference Chat Completion.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a chat completion using Azure AI Inference.
    """
    endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
    key = os.environ["AZURE_INFERENCE_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        temperature=0.7,
        max_tokens=100,
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

This script initializes the Azure Inference client, sends a chat completion request, and prints the response.

## 6. How to run the example code

1. Ensure your environment variables are set:
    - `AZURE_INFERENCE_ENDPOINT`
    - `AZURE_INFERENCE_KEY`
2. Run the script:
    ```bash
    python example.py
    ```

## 7. Next steps

- [Azure AI Inference client library documentation](https://aka.ms/aiservices/inference){:target="_blank"}
- [Azure AI Inference Python SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}
- [OpenAI API documentation](https://platform.openai.com/docs/api-reference/chat/create){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Deploy models with Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}
