# 1. Basic Chat Completion with Azure Inference SDK in Python

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation with an AI model.

## 2. Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services (Azure OpenAI endpoint and key)

## 3. Environment Setup

Follow these steps to set up your environment and install the required libraries.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install the required libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
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
    2. Install the required libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
        export AZURE_OPENAI_CHAT_KEY=<your-api-key>
        ```

## 4. Main Code Components

### 4.1. Import Required Classes

Import the necessary classes from the Azure Inference SDK.

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import os
```

### 4.2. Set Up the Client

Create a client using your Azure OpenAI endpoint and key.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the appropriate API version for your deployment
)
```

### 4.3. Compose the Conversation

Use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure the conversation.

- `SystemMessage`: Sets the behavior or context for the assistant.
- `UserMessage`: Represents a message from the user.
- `AssistantMessage`: Represents a previous message from the assistant (optional, for multi-turn context).

```python
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("What is the capital of France?"),
    AssistantMessage("The capital of France is Paris. How else can I help you?"),
    UserMessage("What is the population of Paris?"),
]
```

### 4.4. Get the Chat Completion

Send the messages to the model and get the response.

```python
response = client.complete(messages=messages)
```

### 4.5. Print the Response

Display the assistant's reply.

```python
print(response.choices[0].message.content)
```

## 5. Complete Example

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
        UserMessage("What is the capital of France?"),
        AssistantMessage("The capital of France is Paris. How else can I help you?"),
        UserMessage("What is the population of Paris?"),
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script sends a short conversation to the Azure OpenAI model, including a system prompt, user questions, and an assistant reply. The model continues the conversation based on the provided context.

## 6. How to Run the Example

1. Save the code to a file, for example, `chat_completion_example.py`.
2. Ensure your environment variables are set as described above.
3. Run the script:
    ```bash
    python chat_completion_example.py
    ```

## 7. Next Steps

- Learn more about [Azure AI Inference SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- Explore [Chat Completions API documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt){:target="_blank"}
- Try adding more message turns or experiment with different system prompts.