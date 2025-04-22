# Basic Chat Completion with Azure Inference SDK in Python

This article shows you how to perform a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to structure a conversation with an AI model deployed on Azure OpenAI.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with a deployed Azure OpenAI model
- The following Python packages:
  - `azure-ai-inference==1.0.0b9`
  - `azure-core==1.33.0`
  - `azure-identity==1.21.0` (if using Entra ID authentication)

## 1. Introduction

You will create a simple script that sends a chat history to an Azure OpenAI model and receives a response. The script demonstrates how to use different message types to simulate a multi-turn conversation.

## 2. Environment Setup

### 2.1. Windows

1. Open **Command Prompt**.
2. Create and activate a virtual environment:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the required packages:
   ```cmd
   pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
   ```
4. Set environment variables:
   ```cmd
   set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
   set AZURE_OPENAI_CHAT_KEY=<your-api-key>
   ```

### 2.2. Linux/macOS

1. Open **Terminal**.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
   ```
4. Set environment variables:
   ```bash
   export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
   export AZURE_OPENAI_CHAT_KEY=<your-api-key>
   ```

## 3. Code Components Breakdown

- **Import libraries**: Import the Azure Inference SDK and message types.
- **Set up the client**: Use your endpoint and API key to authenticate.
- **Create messages**: Use `SystemMessage`, `UserMessage`, and `AssistantMessage` to build a conversation.
- **Send the request**: Call the `complete` method to get a response.
- **Display the result**: Print the assistant's reply.

## 4. Complete Example

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# Get endpoint and key from environment variables
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

# Create the client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the appropriate API version for your deployment
)

# Build the conversation history
messages = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("Hello, who won the FIFA World Cup in 2018?"),
    AssistantMessage("France won the FIFA World Cup in 2018."),
    UserMessage("Who was the top scorer in that tournament?"),
]

# Get the chat completion response
response = client.complete(messages=messages)

# Print the assistant's reply
print("Assistant:", response.choices[0].message.content)
```

## 5. How to Run the Example

1. Save the code to a file, for example, `basic_chat_completion.py`.
2. Ensure your environment variables are set as described above.
3. Run the script:
   ```bash
   python basic_chat_completion.py
   ```

## 6. Next Steps

- Explore the [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}.
- Learn more about [message types and conversation design](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt){:target="_blank"}.
- Try adding more message turns or experiment with different prompts.

---

**Related resources:**
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}
- [Azure AI Inference SDK reference](https://azuresdkdocs.blob.core.windows.net/$web/python/azure-ai-inference/latest/index.html){:target="_blank"}