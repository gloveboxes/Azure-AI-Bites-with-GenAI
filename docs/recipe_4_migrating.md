# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

This guide explains how to migrate your Python code from the OpenAI ChatCompletion API to the Azure Inference Chat Completion API. You will learn about parameter mapping, see code examples for both APIs, and understand the main differences.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

---

## 1. Parameter Mapping: OpenAI vs Azure Inference

The following table shows how common parameters in the OpenAI ChatCompletion API map to the Azure Inference Chat Completion API.

| OpenAI Parameter         | Azure Inference Equivalent         | Notes                                                      |
|--------------------------|------------------------------------|------------------------------------------------------------|
| `model`                  | Set in Azure deployment, not in code| Model is selected via endpoint/deployment in Azure          |
| `messages`               | `messages`                         | Both use a list of message objects                         |
| `temperature`            | `temperature` (optional)           | Supported as an optional parameter                         |
| `max_tokens`             | `max_tokens` (optional)            | Supported as an optional parameter                         |
| `top_p`                  | `top_p` (optional)                 | Supported as an optional parameter                         |
| `stop`                   | `stop` (optional)                  | Supported as an optional parameter                         |
| `api_key`                | `AzureKeyCredential(key)`          | Use AzureKeyCredential for authentication                  |
| `openai.ChatCompletion.create()` | `ChatCompletionsClient.complete()` | Different method names and client initialization           |

---

## 2. Install Dependencies

Set up a Python virtual environment and install the required libraries.

### Windows

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install openai azure-ai-inference==1.0.0b9 azure-core==1.33.0
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai azure-ai-inference==1.0.0b9 azure-core==1.33.0
```

---

## 3. Set Environment Variables

Set the following environment variables for Azure Inference:

- `AZURE_AI_CHAT_ENDPOINT`: Your Azure AI endpoint URL
- `AZURE_AI_CHAT_KEY`: Your Azure AI key

Example (Linux/macOS):

```bash
export AZURE_AI_CHAT_ENDPOINT="https://<your-endpoint>.openai.azure.com/"
export AZURE_AI_CHAT_KEY="<your-azure-key>"
```

Example (Windows):

```cmd
set AZURE_AI_CHAT_ENDPOINT=https://<your-endpoint>.openai.azure.com/
set AZURE_AI_CHAT_KEY=<your-azure-key>
```

---

## 4. Code Example: OpenAI Chat Completion

```python
import openai

openai.api_key = "<your-openai-api-key>"

messages = [
    {"role": "system", "content": "You are an AI assistant that helps people find information. Replies must be ≤2 sentences."},
    {"role": "user", "content": "What year was construction of the international space station mostly done?"}
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message["content"])
```

---

## 5. Code Example: Azure Inference Chat Completion

### Main Components

- **Client Initialization**: Use `ChatCompletionsClient` with your Azure endpoint and key.
- **Message Construction**: Use `SystemMessage`, `UserMessage`, and `AssistantMessage` for chat history.
- **Completion Call**: Call `client.complete(messages=messages)` to get a response.

### Complete Example

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def sample_chat_completions_with_history():
    try:
        endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
        key      = os.environ["AZURE_AI_CHAT_KEY"]
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

## 6. How to Run the Example

1. Activate your virtual environment.
2. Set the required environment variables.
3. Save the Azure Inference code to a file, for example, `azure_chat_completion.py`.
4. Run the script:

```bash
python azure_chat_completion.py
```

---

## 7. Next Steps and Related Resources

- [Azure AI Inference SDK Documentation](https://learn.microsoft.com/azure/ai-services/foundry/)
- [OpenAI Python Library Documentation](https://platform.openai.com/docs/api-reference/chat)
- [Azure AI Foundry Quickstart](https://learn.microsoft.com/azure/ai-services/foundry/quickstart)
- [Azure AI Inference Python SDK Reference](https://pypi.org/project/azure-ai-inference/)

---

By following this guide, you can migrate your chat completion code from OpenAI to Azure Inference with minimal changes. Adjust parameters as needed for your specific use case.