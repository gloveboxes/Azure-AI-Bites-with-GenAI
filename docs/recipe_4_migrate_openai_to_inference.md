# Migrate from OpenAI ChatCompletion API to Azure Inference API

This guide helps you migrate your Python code from the OpenAI ChatCompletion API to the Azure Inference API. You will learn how to set up your environment, map parameters, and update your code to use Azure Inference for chat completions.

---

## 1. Prerequisites

Before you begin, ensure you have:

- An [Azure account](https://portal.azure.com/).
- An Azure AI model deployment with endpoint and key.
- Python 3.8 or later installed.

---

## 2. What You'll Learn

- How to set up a Python virtual environment.
- How to install required Azure Inference libraries.
- How to configure environment variables for authentication.
- How to update your code to use the Azure Inference API.
- How to run your migrated code.

---

## 3. Parameter Mapping: OpenAI vs Azure Inference

| OpenAI ChatCompletion Parameter | Azure Inference API Equivalent         | Notes                                                      |
|---------------------------------|----------------------------------------|------------------------------------------------------------|
| `model`                         | Set in endpoint/deployment             | Model is specified in the Azure endpoint URL.               |
| `input` / `messages`            | `messages` (list of Message objects)   | Use `SystemMessage`, `UserMessage`, `AssistantMessage`.     |
| `api_key`                       | `AZURE_AI_CHAT_KEY` (env variable)     | Set as environment variable, used with `AzureKeyCredential`.|
| `api_base`                      | `AZURE_AI_CHAT_ENDPOINT` (env variable)| Set as environment variable.                                |
| `temperature`, `max_tokens`, etc| Supported as keyword args (optional)   | Pass as arguments to `client.complete()`.                   |
| Response: `output_text`         | `response.choices[0].message.content`  | Access content from the first choice.                       |
| Response: `usage`               | `response.usage`                       | Token usage information.                                    |

---

## 4. Install Dependencies

### 4.1. Create and Activate a Virtual Environment

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

### 4.2. Install Required Packages

```bash
pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0 azure-storage-blob==12.25.1 azure-ai-projects==1.0.0b9
```

---

## 5. Set Environment Variables

Set the following environment variables with your Azure AI endpoint and key.

**Windows (Command Prompt):**
```cmd
set AZURE_AI_CHAT_ENDPOINT=https://<your-deployment-name>.<your-azure-region>.models.ai.azure.com
set AZURE_AI_CHAT_KEY=<your-model-key>
```

**Linux/macOS (Bash):**
```bash
export AZURE_AI_CHAT_ENDPOINT=https://<your-deployment-name>.<your-azure-region>.models.ai.azure.com
export AZURE_AI_CHAT_KEY=<your-model-key>
```

Replace `<your-deployment-name>`, `<your-azure-region>`, and `<your-model-key>` with your actual values.

---

## 6. Code Migration: Main Components

### 6.1. OpenAI Example

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

### 6.2. Azure Inference Example: Main Components

- **Import Libraries:** Import Azure Inference client and message types.
- **Read Environment Variables:** Get endpoint and key from environment.
- **Create Client:** Instantiate `ChatCompletionsClient` with endpoint and credentials.
- **Prepare Messages:** Use `SystemMessage` and `UserMessage` to structure the conversation.
- **Call API:** Use `client.complete()` to get a response.
- **Process Response:** Access the message content and token usage.

---

## 7. Complete Azure Inference Example

```python
import os

def sample_chat_completions():
    try:
        endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_AI_CHAT_KEY"]
    except KeyError:
        print("Missing environment variable 'AZURE_AI_CHAT_ENDPOINT' or 'AZURE_AI_CHAT_KEY'")
        print("Set them before running this sample.")
        exit()

    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("Write a one-sentence bedtime story about a unicorn."),
        ],
    )

    print(response.choices[0].message.content)
    print(f"\nToken usage: {response.usage}")

if __name__ == "__main__":
    sample_chat_completions()
```

---

## 8. How to Run the Example

1. Activate your virtual environment if not already active.
2. Ensure environment variables are set in your current terminal session.
3. Save the code above to a file, for example, `sample_chat_completions.py`.
4. Run the script:

```bash
python sample_chat_completions.py
```

You should see the model's response and token usage printed to the console.

---

## 9. Next Steps and Related Resources

- [Azure Inference Python SDK Documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference)
- [Azure AI Studio](https://ai.azure.com/)
- [Azure AI Inference API Reference](https://learn.microsoft.com/azure/ai-services/inference/)
- [OpenAI to Azure AI Service Migration Guide](https://learn.microsoft.com/azure/ai-services/openai/migration)

---

By following this guide, you can migrate your chat completion workloads from OpenAI to Azure Inference with minimal changes. For advanced scenarios, refer to the Azure Inference SDK documentation.