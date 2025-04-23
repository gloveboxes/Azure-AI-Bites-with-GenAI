# Basic Chat Completion with Azure Inference SDK in Python

## Introduction

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation and get a response from an Azure AI Foundry chat model.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your development environment.

=== "Windows"

    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install required Python libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables. Replace the placeholders with the actual values:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        set AZURE_OPENAI_CHAT_KEY=<your-openai-key>
        ```

=== "Linux/macOS"

    1. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    2. Install required Python libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-openai-key>"
        ```

## 2. Main code components

### 2.1 Import required modules and set up the client

This section imports the necessary modules and initializes the chat completions client using your Azure OpenAI endpoint and key.

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
    api_version="2024-06-01",  # Update as needed
)
```

### 2.2 Compose chat messages

This section demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("How many feet are in a mile?"),
    AssistantMessage("There are 5,280 feet in a mile."),
    UserMessage("How many miles are in a marathon?"),
]
```

### 2.3 Get a chat completion response

This section sends the conversation to the model and prints the assistant's reply.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 3. Complete code example

The following is a complete, functional example that demonstrates a basic chat completion using the Azure Inference SDK.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def basic_chat_completion():
    endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_OPENAI_CHAT_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01",  # Update as needed
    )

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
        AssistantMessage("There are 5,280 feet in a mile."),
        UserMessage("How many miles are in a marathon?"),
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    basic_chat_completion()
```

**Explanation:**  
This script sets up a conversation with a system prompt, a user question, an assistant reply, and a follow-up user question. It sends the conversation to the Azure AI Foundry chat model and prints the assistant's response.

## 4. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the complete code example to a file, for example, `basic_chat_completion.py`.
3. Run the script:
    ```bash
    python basic_chat_completion.py
    ```

## 5. Next steps

- Explore more advanced chat completion features in the [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}.
- Learn how to use structured outputs and function calling with chat completions.
- Review [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"} for more scenarios.