# Basic Chat Completion with Azure AI Inference SDK and Key Authentication

## Introduction

This article demonstrates how to perform a basic chat completion using the Azure AI Inference SDK for Python. You will learn how to authenticate with a key, create a chat client, and use `SystemMessage`, `UserMessage`, and `AssistantMessage` to interact with an AI model deployed via Azure AI Foundry.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with a deployed model endpoint

## 1. Authentication

Azure AI Foundry provides several authentication methods. This example uses **Key Authentication** with the Azure AI Inference SDK.

Azure AI Foundry is a platform for deploying and managing AI models, providing endpoints for inference and integration with Azure services.

To authenticate using a key:

1. Go to your Azure AI Foundry portal.
2. Select your model deployment.
3. From the **SDK** dropdown, select **Azure Inference SDK**.
4. Choose **Authentication type**: Key Authentication.
5. Copy the **Key** and **Endpoint** values for use in your code.

## 2. Developer environment setup

Select your preferred operating system and follow the steps below.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir azure-ai-chat-demo
        cd azure-ai-chat-demo
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
    6. Set up environment variables:
        ```powershell
        $env:AZURE_AI_INFERENCE_ENDPOINT="<your-endpoint-url>"
        $env:AZURE_AI_INFERENCE_KEY="<your-api-key>"
        ```
        Replace the placeholders with the actual values from your Azure AI Foundry deployment.

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir azure-ai-chat-demo
        cd azure-ai-chat-demo
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
    6. Set up environment variables:
        ```bash
        export AZURE_AI_INFERENCE_ENDPOINT="<your-endpoint-url>"
        export AZURE_AI_INFERENCE_KEY="<your-api-key>"
        ```
        Replace the placeholders with the actual values from your Azure AI Foundry deployment.

## 3. Main code components

### a. Import required classes

This section imports the necessary classes for authentication and message construction.

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import os
```

### b. Read endpoint and key from environment

This code reads the endpoint and key from environment variables for secure configuration.

```python
endpoint = os.environ["AZURE_AI_INFERENCE_ENDPOINT"]
key = os.environ["AZURE_AI_INFERENCE_KEY"]
```

### c. Create the chat client

This code creates a synchronous chat completions client using key authentication.

```python
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)
```

### d. Compose chat messages

This code demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to build a conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
    UserMessage("What is the capital of France?")
]
```

### e. Send the chat completion request

This code sends the chat messages to the model and prints the response.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 4. Complete code example

The following is the complete, functional example. Save this as `example.py`.

```python
"""
Basic chat completion using Azure AI Inference SDK with key authentication.

This script demonstrates how to use SystemMessage, UserMessage, and AssistantMessage
to interact with an AI model deployed via Azure AI Foundry.
"""

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a basic chat completion using Azure AI Inference SDK.
    """
    # Read endpoint and key from environment variables
    endpoint = os.environ["AZURE_AI_INFERENCE_ENDPOINT"]
    key = os.environ["AZURE_AI_INFERENCE_KEY"]

    # Create the chat completions client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Compose the conversation using SystemMessage, UserMessage, and AssistantMessage
    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
        UserMessage("What is the capital of France?")
    ]

    # Send the chat completion request
    response = client.complete(messages=messages)

    # Print the assistant's reply
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

The assistant's reply to the last user message will be printed to the console.

## 6. Next steps

- Explore the [Azure AI Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}
- Review [Azure AI Inference Python API reference](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}
- Learn more about [message types](https://aka.ms/azsdk/azure-ai-inference/python/reference#azure.ai.inference.models.SystemMessage){:target="_blank"}
- Try advanced features such as streaming, model parameters, or structured output

For more code samples, visit the [Azure AI Inference SDK samples repository](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}.