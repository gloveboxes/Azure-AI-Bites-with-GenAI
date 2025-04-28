# Basic Chat Completion with Azure AI Inference SDK and Key Authentication

## Introduction

This guide shows you how to perform a basic chat completion using the Azure AI Inference SDK in Python. You will use key authentication and demonstrate how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to interact with a chat model deployed in Azure AI Foundry.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with a deployed chat model

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a new project folder:
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
        $env:AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-key>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a new project folder:
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
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>"
        export AZURE_OPENAI_CHAT_KEY="<your-key>"
        ```

**Note:** Replace the placeholders with your actual Azure OpenAI endpoint and key.

## 2. Azure AI Services

Azure AI Foundry provides access to a catalog of AI models, including chat models, which you can deploy and use for inference. The Azure AI Inference SDK allows you to interact with these models programmatically.

**Authentication:**

- This example uses Key Authentication.
- You need your model deployment's **Key** and **Endpoint**.

To find your authentication key and endpoint:

- In the Azure AI Foundry portal, select your deployment.
- From the **SDK** dropdown, select **Azure Inference SDK**.
- Select **Authentication type**: Key Authentication.
- The **Key** and **Endpoint** are displayed.

## 3. Main code components

### 3.1 Import required modules and set up the client

This section imports the necessary modules and initializes the chat completions client using your endpoint and key.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
```

### 3.2 Prepare chat messages

You will create a list of messages to send to the model, including a system message, a user message, and (optionally) an assistant message.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    # Optionally, you can add an AssistantMessage to continue a conversation
    # AssistantMessage("There are 5,280 feet in a mile."),
]
```

### 3.3 Send the chat completion request

This section sends the messages to the model and prints the response.

```python
client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_OPENAI_CHAT_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_OPENAI_CHAT_KEY"]),
    api_version="2024-06-01",  # Use the API version appropriate for your deployment
)

response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 4. Complete code example

Save the following code as `example.py`. This script demonstrates a basic chat completion using the Azure AI Inference SDK and key authentication.

```python
"""
example.py

This script demonstrates how to perform a basic chat completion using the Azure AI Inference SDK
with key authentication. It shows how to use SystemMessage, UserMessage, and AssistantMessage
to interact with a deployed chat model in Azure AI Foundry.

Environment variables required:
- AZURE_OPENAI_CHAT_ENDPOINT: The endpoint URL for your Azure OpenAI deployment.
- AZURE_OPENAI_CHAT_KEY: The API key for your deployment.
"""

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Run a basic chat completion using Azure AI Inference SDK.
    """
    try:
        endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_OPENAI_CHAT_KEY"]
    except KeyError:
        print("Please set the AZURE_OPENAI_CHAT_ENDPOINT and AZURE_OPENAI_CHAT_KEY environment variables.")
        return

    # Initialize the client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01",
    )

    # Prepare the chat messages
    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        # You can add an AssistantMessage to continue a conversation, for example:
        # AssistantMessage("There are 5,280 feet in a mile."),
    ]

    # Get the chat completion response
    response = client.complete(messages=messages)

    # Print the assistant's reply
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

## 5. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the code above as `example.py`.
3. Run the script:

    ```bash
    python example.py
    ```

You should see the assistant's response printed to the console.

## 6. Next steps

- [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}