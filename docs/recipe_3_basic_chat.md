# Basic Chat Completion with Azure AI Inference SDK and Key Authentication

## Introduction

This article demonstrates how to perform a basic chat completion using the Azure AI Inference SDK for Python. You will learn how to authenticate with a key, create a chat client, and use `SystemMessage`, `UserMessage`, and `AssistantMessage` to interact with an AI model deployed via Azure AI Foundry.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with a deployed model endpoint and API key

## 1. Authentication

Azure AI Foundry provides secure access to deployed AI models using key authentication. You will need your model's endpoint URL and API key, which can be found in the Azure AI Foundry portal under your deployment's **SDK** section.

1. Go to your Azure AI Foundry deployment in the portal.
2. Select **Azure Inference SDK** from the SDK dropdown.
3. Choose **Key Authentication** as the authentication type.
4. Copy the **Key** and **Endpoint** values for use in your application.

## 2. Developer environment setup

Select your preferred operating system:

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
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_AI_INFERENCE_ENDPOINT = "<your-endpoint-url>"
        $env:AZURE_AI_INFERENCE_KEY = "<your-api-key>"
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

### Set up authentication and client

This code retrieves the endpoint and key from environment variables and creates a chat completions client using key authentication.

```python
endpoint = os.environ["AZURE_AI_INFERENCE_ENDPOINT"]
key = os.environ["AZURE_AI_INFERENCE_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)
```

### Create and send chat messages

This code demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
    UserMessage("What is the capital of France?")
]

response = client.complete(messages=messages)
```

### Print the response

This code prints the assistant's reply and token usage.

```python
print("Assistant:", response.choices[0].message.content)
print("Token usage:", response.usage)
```

## 4. Complete code example

The following is the complete example. Save this code as `example.py`.

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
    # Retrieve endpoint and key from environment variables
    endpoint = os.environ["AZURE_AI_INFERENCE_ENDPOINT"]
    key = os.environ["AZURE_AI_INFERENCE_KEY"]

    # Create the chat completions client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Define the conversation messages
    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        AssistantMessage("There are 5,280 feet in a mile. How else can I help you?"),
        UserMessage("What is the capital of France?")
    ]

    # Get the chat completion response
    response = client.complete(messages=messages)

    # Print the assistant's reply and token usage
    print("Assistant:", response.choices[0].message.content)
    print("Token usage:", response.usage)

if __name__ == "__main__":
    main()
```

## 5. How to run the example code

1. Ensure your virtual environment is activated and environment variables are set.
2. Run the script:

    ```bash
    python example.py
    ```

You should see the assistant's response to the last user message and token usage information.

## 6. Next steps

- Explore more chat completion features in the [Azure AI Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}.
- Review additional [Python samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}.
- Learn about [message types](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"} and advanced conversation patterns.
- For troubleshooting, see [Configure logging in the Azure libraries for Python](https://aka.ms/azsdk/python/logging){:target="_blank"}.

---

**Related resources:**

- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Azure AI Inference SDK API reference](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}
- [Azure AI Inference SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}