# Basic Chat Completion with Azure Inference SDK in Python

## Introduction

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation and get a response from an Azure AI model.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows"

    1. Open **Command Prompt** or **PowerShell**.
    2. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    3. Install the required Python libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    4. Set the required environment variables. Replace the placeholders with the actual values:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        set AZURE_OPENAI_CHAT_KEY=<your-model-key>
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    3. Install the required Python libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    4. Set the required environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-model-key>"
        ```

## 2. Main code components

### 2.1 Import required modules and set up the client

This section imports the necessary modules and sets up the `ChatCompletionsClient` using your Azure OpenAI endpoint and key.

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

This section demonstrates how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("What is the capital of France?"),
    AssistantMessage("The capital of France is Paris. How else can I help you?"),
    UserMessage("What is the population of Paris?")
]
```

### 2.3 Send the chat completion request and handle the response

This section sends the conversation to the model and prints the assistant's reply.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

## 3. Complete code example

The following is the complete code example that brings together all the components described above.

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
        AssistantMessage("The capital of France is Paris. How else can I help you?"),
        UserMessage("What is the population of Paris?")
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script sets up the Azure Inference client, structures a conversation using different message types, sends the conversation to the model, and prints the assistant's response.

## 4. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the complete code example to a file, for example, `chat_completion_example.py`.
3. Run the script:

    ```bash
    python chat_completion_example.py
    ```

## Next steps

- Explore more message types and conversation flows in the [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}.
- Learn how to use advanced features such as function calling and structured outputs.
- Review [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"} for more information.