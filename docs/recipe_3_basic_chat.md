# Basic Chat Completion with Azure AI Inference SDK and Key Authentication

## Introduction

This article demonstrates how to perform a basic chat completion using the Azure AI Inference SDK in Python. You will learn how to authenticate using a key and endpoint, and how to use different message types such as `SystemMessage`, `UserMessage`, and `AssistantMessage` to interact with an AI model deployed in Azure AI Foundry.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with a deployed model

## 1. Authentication

This example uses the Azure AI Inference SDK and Key Authentication.

Key Authentication requires an endpoint URL and an API key. The endpoint is the URL of your deployed model in Azure AI Foundry. The API key is a secret used to authenticate your requests.

To obtain your endpoint and key:

1. Go to the Azure AI Foundry portal.
2. Select your model deployment.
3. From the **SDK** dropdown, select **Azure Inference SDK**.
4. Under **Authentication type**, select **Key Authentication**.
5. Copy the **Endpoint** and **Key** values.

## 2. Developer environment setup

Select your preferred operating system:

=== "Windows (PowerShell)"
    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir azure-ai-chat-sample
        cd azure-ai-chat-sample
        ```
    3. Set up a virtual environment:
        ```powershell
        python -m venv .venv
        ```
    4. Activate the virtual environment:
        ```powershell
        .venv\Scripts\Activate
        ```
    5. Install the required libraries:
        ```powershell
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_AI_INFERENCE_ENDPOINT = "<your-endpoint-url>"
        $env:AZURE_AI_INFERENCE_KEY = "<your-api-key>"
        ```

=== "Linux/macOS"
    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir azure-ai-chat-sample
        cd azure-ai-chat-sample
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
        export AZURE_AI_INFERENCE_ENDPOINT="<your-endpoint-url>"
        export AZURE_AI_INFERENCE_KEY="<your-api-key>"
        ```

## 3. Main code components

### Import required libraries

This section imports the necessary Python libraries for authentication and chat completion.

```python
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
```

### Set up the client

This code retrieves the endpoint and key from environment variables and creates a `ChatCompletionsClient` for interacting with the Azure AI model.

```python
endpoint = os.environ["AZURE_AI_INFERENCE_ENDPOINT"]
key = os.environ["AZURE_AI_INFERENCE_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)
```

### Compose chat messages

This code demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
    UserMessage("What is the capital of France?")
]
```

### Send the chat completion request

This code sends the messages to the model and prints the response.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 4. Complete code example

The following is the complete code sample. Save this as `example.py`.

```python
"""
Basic chat completion using Azure AI Inference SDK and Key Authentication.

This script demonstrates how to use SystemMessage, UserMessage, and AssistantMessage
to interact with an AI model deployed in Azure AI Foundry.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a basic chat completion using Azure AI Inference SDK.
    """
    endpoint = os.environ["AZURE_AI_INFERENCE_ENDPOINT"]
    key = os.environ["AZURE_AI_INFERENCE_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
        UserMessage("What is the capital of France?")
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

## 5. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Run the script:
    ```bash
    python example.py
    ```

## 6. Next steps

- Learn more about [Azure AI Inference client library for Python](https://aka.ms/aiservices/inference){:target="_blank"}
- Explore [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-studio/){:target="_blank"}
- Review [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}
- See more [Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}