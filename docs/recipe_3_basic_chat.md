# Basic Chat Completion with Azure Inference SDK in Python

## Introduction

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation and get a response from an Azure OpenAI model.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (such as **PowerShell**).
    2. Create a new project folder:
        ```powershell
        mkdir azure-chat-sample
        cd azure-chat-sample
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
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-openai-key>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a new project folder:
        ```bash
        mkdir azure-chat-sample
        cd azure-chat-sample
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
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-openai-key>"
        ```

> **Note:** Replace the placeholders with your actual Azure OpenAI endpoint and key.

## 2. Main code components

### 2.1 Import required modules and set up the client

This section imports the necessary modules and sets up the chat completions client using your Azure OpenAI endpoint and key.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01"
)
```

### 2.2 Compose the conversation with message types

This section demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation. The system message sets the assistant's behavior, the user message asks a question, and the assistant message can be used to provide context or continue a conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("What is the capital of France?"),
    AssistantMessage("The capital of France is Paris. Do you want to know more?")
]
```

### 2.3 Send the chat completion request and print the response

This section sends the conversation to the model and prints the assistant's reply.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 3. Complete code example

The following is the complete code example. Save this as `example.py`.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():
    endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_OPENAI_CHAT_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01"
    )

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("What is the capital of France?"),
        AssistantMessage("The capital of France is Paris. Do you want to know more?")
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

This script sets up the client, structures a conversation using the three message types, sends the request, and prints the assistant's response.

## 4. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Run the script:

    ```bash
    python example.py
    ```

You should see the assistant's response printed in the terminal.

## 5. Next steps

- [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}
- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}