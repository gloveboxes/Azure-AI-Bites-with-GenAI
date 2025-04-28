# Basic Chat Completion with Azure AI Inference SDK and Key Authentication

## Introduction

This article shows you how to perform a basic chat completion using the Azure AI Inference SDK in Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation, and how to authenticate using an API key.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

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
        .venv\Scripts\Activate
        ```
    5. Install the required libraries:
        ```powershell
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-api-key>"
        ```

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
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-api-key>"
        ```

## 2. Azure AI Services

Azure AI Foundry provides access to a wide range of AI models and services, including chat completion models. The Azure AI Inference SDK allows you to interact with these models programmatically.

**Authentication:**
- This example uses Key Authentication.
- To find your authentication key and endpoint:
    1. In the Azure AI Foundry portal, select your deployment.
    2. From the **SDK** dropdown, select **Azure Inference SDK**.
    3. Select **Authentication type**: Key Authentication. The **Key** and **Endpoint** are displayed.

## 3. Main code components

### a. Import required modules and set up authentication

This section imports the necessary modules and retrieves the endpoint and key from environment variables.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
```

### b. Create the chat client

This code creates a `ChatCompletionsClient` using the endpoint and key.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the appropriate API version for your deployment
)
```

### c. Compose the conversation

This section demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure the conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    # Optionally, you can add an AssistantMessage to continue a conversation
    # AssistantMessage("There are 5280 feet in a mile."),
]
```

### d. Get the chat completion response

This code sends the messages to the model and prints the assistant's reply.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 4. Complete code example

Save the following code as `example.py`.

```python
"""
Basic chat completion using Azure AI Inference SDK with Key Authentication.

This script demonstrates how to use SystemMessage, UserMessage, and AssistantMessage
to structure a conversation and get a response from an Azure OpenAI deployment.
"""

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a basic chat completion using Azure AI Inference SDK.
    """
    # Retrieve endpoint and key from environment variables
    endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_OPENAI_CHAT_KEY"]

    # Create the chat completions client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01",
    )

    # Compose the conversation
    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        # You can add an AssistantMessage to continue the conversation if needed
        # AssistantMessage("There are 5280 feet in a mile."),
    ]

    # Get the chat completion response
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

The assistant's response will be printed to the console.

## 6. Next steps

- [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}