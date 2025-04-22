# 1. Basic Chat Completion with Azure Inference SDK

This guide shows you how to generate a basic chat completion in Python using the Azure Inference SDK. You will learn how to use `SystemMessage`, `UserMessage`, and `AssistantMessage` to create a conversational history for chat completions.

## 2. Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 3. Install Dependencies

Follow these steps to set up your environment and install the required libraries.

### 3.1. Create and Activate a Virtual Environment

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.2. Install Required Python Packages

```bash
pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
```

### 3.3. Set Environment Variables

Set the following environment variables with your Azure AI Foundry endpoint and key.

**Windows (Command Prompt):**
```cmd
set AZURE_AI_CHAT_ENDPOINT=<your-endpoint>
set AZURE_AI_CHAT_KEY=<your-key>
```

**Linux/macOS:**
```bash
export AZURE_AI_CHAT_ENDPOINT=<your-endpoint>
export AZURE_AI_CHAT_KEY=<your-key>
```

Replace `<your-endpoint>` and `<your-key>` with your actual Azure AI Foundry values.

## 4. Understanding the Main Code Components

The example code demonstrates:

- **SystemMessage**: Sets the behavior and context for the AI assistant.
- **UserMessage**: Represents a message from the user.
- **AssistantMessage**: Represents a message from the assistant, used to maintain conversation history.
- **ChatCompletionsClient**: The main client to interact with the Azure Inference chat completion service.
- **Conversation History**: By appending messages, you maintain context across multiple turns.

## 5. Complete Code Example

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

    # First turn: set up system and user messages
    messages = [
        SystemMessage("You are an AI assistant that helps people find information. Replies must be ≤2 sentences."),
        UserMessage("What year was construction of the international space station mostly done?")
    ]
    response = client.complete(messages=messages)
    print("Assistant:", response.choices[0].message.content)

    # Second turn: add assistant's reply and another user message
    messages.append(AssistantMessage(response.choices[0].message.content))
    messages.append(UserMessage("And what was the estimated cost to build it?"))
    response = client.complete(messages=messages)
    print("Assistant:", response.choices[0].message.content)

if __name__ == "__main__":
    sample_chat_completions_with_history()
```

## 6. How to Run the Example Code

1. Activate your virtual environment if not already active.
2. Ensure your environment variables are set.
3. Save the code to a file, for example, `chat_completion_example.py`.
4. Run the script:

```bash
python chat_completion_example.py
```

You will see the assistant's responses printed to the console.

## 7. Next Steps

- Explore the [Azure AI Inference SDK documentation](https://learn.microsoft.com/azure/ai-services/foundry/) for more advanced features.
- Try adding more conversation turns or modifying the system prompt.
- Review other message types and capabilities in the SDK.

---

**Related resources:**
- [Azure AI Inference SDK Reference](https://pypi.org/project/azure-ai-inference/)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-services/foundry/)