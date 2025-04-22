# 1. Basic Chat Completion with Azure Inference SDK in Python

This guide shows you how to generate a basic chat completion using the Azure Inference SDK for Python. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to create a conversational history for your AI assistant.

## 2. Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services (with a deployed chat model)
- The following Python libraries:
  - `azure-ai-inference==1.0.0b9`
  - `azure-core==1.33.0`

## 3. What You'll Learn

- How to set up a Python virtual environment
- How to install required libraries
- How to set environment variables for authentication
- How to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to build a chat history
- How to run a basic chat completion

---

## 4. Environment Setup

### 4.1. Windows

1. **Create and activate a virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install required libraries:**
   ```cmd
   pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
   ```

3. **Set environment variables:**
   ```cmd
   set AZURE_AI_CHAT_ENDPOINT=<your-endpoint>
   set AZURE_AI_CHAT_KEY=<your-key>
   ```

### 4.2. Linux/macOS

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install required libraries:**
   ```bash
   pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
   ```

3. **Set environment variables:**
   ```bash
   export AZURE_AI_CHAT_ENDPOINT=<your-endpoint>
   export AZURE_AI_CHAT_KEY=<your-key>
   ```

---

## 5. Main Code Components

### 5.1. Import Required Libraries

You need to import the Azure Inference SDK and supporting modules.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
```

### 5.2. Set Up the Client

You create a `ChatCompletionsClient` using your endpoint and key.

```python
endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
key = os.environ["AZURE_AI_CHAT_KEY"]
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
```

### 5.3. Build the Message History

- `SystemMessage` sets the assistant's behavior.
- `UserMessage` represents user input.
- `AssistantMessage` represents the assistant's previous response.

```python
messages = [
    SystemMessage("You are an AI assistant that helps people find information. Replies must be ≤2 sentences."),
    UserMessage("What year was construction of the international space station mostly done?")
]
```

### 5.4. Get a Chat Completion

You send the message history to the model and print the response.

```python
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

### 5.5. Add to the Conversation History

You can add the assistant's reply and continue the conversation.

```python
messages.append(AssistantMessage(response.choices[0].message.content))
messages.append(UserMessage("And what was the estimated cost to build it?"))
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```

---

## 6. Complete Example

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def sample_chat_completions_with_history():
    try:
        endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_AI_CHAT_KEY"]
    except KeyError:
        print("Missing AZURE_AI_CHAT_ENDPOINT or AZURE_AI_CHAT_KEY")
        exit(1)

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # First turn
    messages = [
        SystemMessage("You are an AI assistant that helps people find information. Replies must be ≤2 sentences."),
        UserMessage("What year was construction of the international space station mostly done?")
    ]
    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

    # Second turn (history included)
    messages.append(AssistantMessage(response.choices[0].message.content))
    messages.append(UserMessage("And what was the estimated cost to build it?"))
    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    sample_chat_completions_with_history()
```

---

## 7. How to Run the Example

1. Save the code to a file, for example, `chat_completion_example.py`.
2. Ensure your environment variables are set.
3. Run the script:

   ```bash
   python chat_completion_example.py
   ```

---

## 8. Next Steps

- [Azure AI Inference SDK documentation](https://learn.microsoft.com/azure/ai-services/foundry/)
- [Azure AI Foundry Quickstart](https://learn.microsoft.com/azure/ai-services/foundry/quickstart)
- [ChatCompletionsClient reference](https://learn.microsoft.com/python/api/overview/azure/ai-inference-readme)

You can now build more advanced conversational experiences by extending the message history and handling more complex user interactions.