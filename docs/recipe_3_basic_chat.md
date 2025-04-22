# Basic Chat Completion with Azure Inference SDK in Python

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation with an AI model deployed on Azure AI Foundry.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with a deployed chat model (such as GPT-4o or GPT-3.5)
- Your Azure OpenAI endpoint and API key

## 1. Introduction

You will create a simple chat session with the Azure Inference SDK, sending a system prompt, a user message, and an assistant message as context. The assistant will then generate a response.

## 2. Environment Setup

Follow these steps to set up your Python environment and required libraries.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install required libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    3. Set environment variables:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
        set AZURE_OPENAI_CHAT_KEY=<your-api-key>
        ```

=== "Linux/macOS"
    1. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    2. Install required libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
        ```
    3. Set environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
        export AZURE_OPENAI_CHAT_KEY=<your-api-key>
        ```

## 3. Main Code Components

### 3.1 Import Required Classes

Import the necessary classes from the Azure Inference SDK.

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import os
```

### 3.2 Initialize the Client

Create a client using your endpoint and API key.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the appropriate API version for your deployment
)
```

### 3.3 Compose the Conversation

Use `SystemMessage`, `UserMessage`, and `AssistantMessage` to provide context and conversation history.

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("Who won the FIFA World Cup in 2018?"),
    AssistantMessage("France won the FIFA World Cup in 2018."),
    UserMessage("Who was the top scorer in that tournament?"),
]
```

### 3.4 Get the Chat Completion

Send the conversation to the model and get the assistant's response.

```python
response = client.complete(messages=messages)
assistant_reply = response.choices[0].message.content
print(assistant_reply)
```

## 4. Complete Example

Here is the complete code example:

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
        api_version="2024-06-01",
    )

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("Who won the FIFA World Cup in 2018?"),
        AssistantMessage("France won the FIFA World Cup in 2018."),
        UserMessage("Who was the top scorer in that tournament?"),
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script sets up a conversation with context, including a system prompt, a user question, and an assistant's previous answer. It then asks a follow-up question and prints the assistant's response.

## 5. How to Run the Example

1. Ensure your environment variables are set as shown in the setup section.
2. Save the code to a file, for example, `basic_chat_completion.py`.
3. Run the script:
    ```bash
    python basic_chat_completion.py
    ```

## 6. Next Steps

- Explore [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}.
- Learn about [advanced chat completion features](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-python){:target="_blank"}.
- Try adding more message types or experiment with different system prompts.