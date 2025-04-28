# Basic Chat Completion with Azure Inference SDK and Key Authentication

## Introduction

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will use key authentication and the `SystemMessage`, `UserMessage`, and `AssistantMessage` message types to interact with an Azure AI Foundry chat model.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir azure-inference-chat
        cd azure-inference-chat
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
        $env:AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-key>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir azure-inference-chat
        cd azure-inference-chat
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
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>"
        export AZURE_OPENAI_CHAT_KEY="<your-key>"
        ```

## 2. Azure AI Services

Azure AI Foundry provides access to a catalog of AI models, including chat models, for building generative AI applications. The Azure Inference SDK allows you to interact with these models using Python.

**Authentication:**  
This example uses key authentication.  
- To find your **Key** and **Endpoint**:
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

### c. Compose the chat messages

This code demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure the conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
    UserMessage("How many meters is that?"),
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
Basic chat completion using Azure Inference SDK with key authentication.

This script demonstrates how to use SystemMessage, UserMessage, and AssistantMessage
to interact with an Azure AI Foundry chat model.
"""

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a basic chat completion using Azure Inference SDK.
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

    # Compose the conversation using message types
    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
        UserMessage("How many meters is that?"),
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