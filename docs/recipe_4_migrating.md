# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This guide explains how to migrate your code from using the OpenAI Chat Completion API to the Azure AI Inference Chat Completion API. You will learn about the differences in API parameters, authentication, and see side-by-side code examples to help you update your applications.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Foundry provides secure access to AI models through key-based authentication or Microsoft Entra ID. For the Azure Inference SDK, you typically use key authentication.

To obtain your endpoint and key:

1. Go to the Azure AI Foundry portal.
2. Select your deployment.
3. From the **SDK** dropdown, select **Azure Inference SDK**.
4. Choose **Authentication type** as **Key Authentication**.
5. Copy the **Key** and **Endpoint** values.

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
        pip install openai==1.30.5 azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables:
        ```powershell
        $env:AZURE_INFERENCE_ENDPOINT="<your-endpoint>"
        $env:AZURE_INFERENCE_KEY="<your-key>"
        ```
        Replace the placeholders with the actual values.

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
        pip install openai==1.30.5 azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables:
        ```bash
        export AZURE_INFERENCE_ENDPOINT="<your-endpoint>"
        export AZURE_INFERENCE_KEY="<your-key>"
        ```
        Replace the placeholders with the actual values.

## 3. API Mapping

The following table maps the key parameters between the OpenAI ChatCompletion API and the Azure Inference Chat Completion API.

| OpenAI Parameter         | Azure Inference Parameter         | Notes                                                      |
|------------------------- |----------------------------------|------------------------------------------------------------|
| `model`                  | (set at client or per call)      | Azure Inference: set at client creation or in `complete()` |
| `messages`               | `messages`                       | Same structure; supports dict or strongly-typed classes    |
| `temperature`            | `temperature`                    | Same meaning                                               |
| `max_tokens`             | `max_tokens`                     | Same meaning                                               |
| `top_p`                  | `top_p`                          | Same meaning                                               |
| `n`                      | `n`                              | Same meaning                                               |
| `stop`                   | `stop`                           | Same meaning                                               |
| `stream`                 | `stream`                         | Same meaning                                               |
| `presence_penalty`       | `presence_penalty`               | Same meaning                                               |
| `frequency_penalty`      | `frequency_penalty`              | Same meaning                                               |
| `logit_bias`             | `logit_bias`                     | Same meaning                                               |
| `user`                   | `user`                           | Same meaning                                               |
| `api_key` (in client)    | `AzureKeyCredential(key)`        | Azure Inference uses AzureKeyCredential                    |
| `base_url` (in client)   | `endpoint`                       | Azure Inference uses `endpoint`                            |
| `response_format`        | `response_format`                | Supported in Azure Inference                               |

For a full list of supported parameters, see the [Azure AI Inference Python SDK reference](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}.

## 4. Main code components

### 4.1 OpenAI Chat Completion Example

This example shows how to use the OpenAI Python SDK to get a chat completion.

```python
"""
Get a chat completion using the OpenAI Python SDK.
"""

import os

import openai

def openai_chat_completion():
    # Set your OpenAI API key and endpoint if needed
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # openai.api_base = "<your-openai-endpoint>"  # Optional for Azure OpenAI

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "How many feet are in a mile?"},
        ],
        temperature=0.7,
        max_tokens=100,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    openai_chat_completion()
```

### 4.2 Azure Inference Chat Completion Example

This example shows how to use the Azure AI Inference SDK to get a chat completion.

```python
"""
Get a chat completion using the Azure AI Inference SDK.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def azure_inference_chat_completion():
    endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT")
    key = os.getenv("AZURE_INFERENCE_KEY")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        # model="gpt-3.5-turbo",  # Optional: set model here or in complete()
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
    azure_inference_chat_completion()
```

## 5. Complete code

Below is a complete example for Azure Inference. Save this as `example.py`.

```python
"""
example.py

Get a chat completion using the Azure AI Inference SDK.

This script demonstrates how to migrate from OpenAI ChatCompletion to Azure Inference ChatCompletion.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a chat completion using Azure AI Inference.
    """
    endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT")
    key = os.getenv("AZURE_INFERENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Please set AZURE_INFERENCE_ENDPOINT and AZURE_INFERENCE_KEY environment variables.")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
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

Save this file as `example.py`.

## 6. How to run the example code

1. Ensure your environment variables are set:
    - `AZURE_INFERENCE_ENDPOINT`
    - `AZURE_INFERENCE_KEY`
2. Run the script:
    ```bash
    python example.py
    ```

## 7. Next steps

- [Azure AI Inference Python SDK documentation](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}
- [Azure AI Inference samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}
- [OpenAI Python SDK documentation](https://platform.openai.com/docs/api-reference/chat/create){:target="_blank"}
- [Deploy models with Azure AI Foundry](https://learn.microsoft.com/azure/ai-studio/concepts/deployments-overview){:target="_blank"}