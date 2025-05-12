# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This article explains how to migrate your code from using the OpenAI Chat Completion API to the Azure AI Inference Chat Completion API. You will learn about the differences in API parameters, authentication, and see code samples for both services. The goal is to help you transition your chat completion workloads to Azure AI Foundry with minimal changes.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Inference supports several authentication methods. This example uses Key Authentication with the Inference SDK.

Key Authentication requires an **Endpoint** and an **API Key**. You can obtain these from the Azure AI Foundry portal:

1. Go to your Azure AI Foundry deployment in the portal.
2. From the **SDK** dropdown, select **Azure Inference SDK**.
3. Choose **Authentication type**: Key Authentication.
4. Copy the **Key** and **Endpoint** values displayed.

## 2. Developer environment setup

Select your preferred operating system.

=== "Windows (PowerShell)"

    1. Open a terminal.
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
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:OPENAI_API_KEY = "<your-openai-api-key>"
        $env:AZURE_INFERENCE_ENDPOINT = "<your-azure-inference-endpoint>"
        $env:AZURE_INFERENCE_KEY = "<your-azure-inference-key>"
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
        pip install openai==1.30.5 azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export OPENAI_API_KEY="<your-openai-api-key>"
        export AZURE_INFERENCE_ENDPOINT="<your-azure-inference-endpoint>"
        export AZURE_INFERENCE_KEY="<your-azure-inference-key>"
        ```

## 3. API Mapping

The following table maps the key parameters between the OpenAI ChatCompletion API and the Azure Inference Chat Completion API.

| OpenAI Parameter         | Azure Inference Parameter         | Notes                                                      |
|-------------------------|-----------------------------------|------------------------------------------------------------|
| `model`                 | (set at client or per call)       | Azure Inference: set at client creation or in `complete()` |
| `messages`              | `messages`                        | Same structure; supports dict or strongly-typed classes    |
| `temperature`           | `temperature`                     | Same meaning                                               |
| `max_tokens`            | `max_tokens`                      | Same meaning                                               |
| `top_p`                 | `top_p`                           | Same meaning                                               |
| `n`                     | `n`                               | Same meaning                                               |
| `stop`                  | `stop`                            | Same meaning                                               |
| `stream`                | `stream`                          | Same meaning                                               |
| `presence_penalty`      | `presence_penalty`                | Same meaning                                               |
| `frequency_penalty`     | `frequency_penalty`               | Same meaning                                               |
| `logit_bias`            | `logit_bias`                      | Same meaning                                               |
| `user`                  | `user`                            | Same meaning                                               |
| `api_key` (in client)   | `credential=AzureKeyCredential()` | Azure Inference uses AzureKeyCredential                    |
| `base_url` (in client)  | `endpoint`                        | Azure Inference uses `endpoint`                            |

For a full list of supported parameters, see the [OpenAI API reference](https://platform.openai.com/docs/api-reference/chat){:target="_blank"} and [Azure AI Inference API reference](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}.

## 4. Code Sample

This section shows how to call the OpenAI ChatCompletion API and the equivalent Azure Inference Chat Completion API.

### OpenAI ChatCompletion Example

This example uses the OpenAI Python SDK to get a chat completion.

```python
"""
Get a chat completion using the OpenAI API.
"""

import os

import openai

def openai_chat_completion():
    # Set up OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]

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

### Azure Inference Chat Completion Example

This example uses the Azure AI Inference SDK to get a chat completion.

```python
"""
Get a chat completion using the Azure AI Inference SDK.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def azure_inference_chat_completion():
    endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
    key = os.environ["AZURE_INFERENCE_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        # Optionally set default parameters here
        # temperature=0.7,
        # max_tokens=100,
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

Below is a complete example that includes both OpenAI and Azure Inference chat completion functions. Save this as `example.py`.

```python
"""
Module: example.py

This module demonstrates how to migrate from OpenAI ChatCompletion to Azure Inference Chat Completion.
"""

import os

import openai

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def openai_chat_completion():
    """
    Get a chat completion using the OpenAI API.
    """
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "How many feet are in a mile?"},
        ],
        temperature=0.7,
        max_tokens=100,
    )

    print("OpenAI response:")
    print(response.choices[0].message.content)

def azure_inference_chat_completion():
    """
    Get a chat completion using the Azure AI Inference SDK.
    """
    endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
    key = os.environ["AZURE_INFERENCE_KEY"]

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

    print("Azure Inference response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    print("Running OpenAI ChatCompletion example...")
    openai_chat_completion()
    print("\nRunning Azure Inference Chat Completion example...")
    azure_inference_chat_completion()
```

## 6. How to run the example code

1. Ensure your environment variables are set as described in the developer environment setup.
2. Save the code above as `example.py`.
3. Run the script:
    ```bash
    python example.py
    ```

## Next steps

- [Azure AI Inference Python SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}
- [OpenAI API reference](https://platform.openai.com/docs/api-reference/chat){:target="_blank"}
- [Azure AI Inference API reference](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-studio/){:target="_blank"}
- [Samples for Azure AI Inference](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}
