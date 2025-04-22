# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

This guide explains how to migrate your code from the OpenAI `ChatCompletion` API to the Azure Inference `ChatCompletionsClient`. It includes a parameter mapping table and code examples for both APIs.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Parameter Mapping: OpenAI vs Azure Inference

| OpenAI `ChatCompletion` Parameter | Azure Inference `ChatCompletionsClient.complete` Parameter | Notes                                                                                 |
|-----------------------------------|------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `model`                          | Set in endpoint URL                                        | Azure uses deployment name in the endpoint URL, not as a parameter                    |
| `messages`                       | `messages`                                                 | Both use the same message format (list of dicts or message objects)                   |
| `temperature`                    | `temperature`                                              | Supported                                                                             |
| `top_p`                          | `top_p`                                                    | Supported                                                                             |
| `max_tokens`                     | `max_tokens`                                               | Supported                                                                             |
| `stop`                           | `stop`                                                     | Supported                                                                             |
| `n`                              | `n`                                                        | Supported                                                                             |
| `stream`                         | `stream`                                                   | Supported                                                                             |
| `presence_penalty`               | `presence_penalty`                                         | Supported                                                                             |
| `frequency_penalty`              | `frequency_penalty`                                        | Supported                                                                             |
| `logit_bias`                     | `logit_bias`                                               | Supported                                                                             |
| `user`                           | `user`                                                     | Supported                                                                             |
| `functions` / `tools`            | `tools`                                                    | Supported (for function calling)                                                      |
| `function_call` / `tool_choice`  | `tool_choice`                                              | Supported                                                                             |
| `response_format`                | `response_format`                                          | Supported (for structured output)                                                     |
| `api_key`                        | `credential`                                               | Use `AzureKeyCredential` or `DefaultAzureCredential`                                  |
| `base_url`                       | `endpoint`                                                 | Azure endpoint includes deployment name                                               |
| `api_version`                    | `api_version`                                              | Required for Azure Inference                                                          |

> **Note:** Some advanced OpenAI parameters or features may not be available or may have different behaviors in Azure. Always consult the [Azure Inference documentation](https://learn.microsoft.com/azure/ai-services/openai/reference) for the latest details.

---

## 2. Environment Setup

Set up your Python environment and install the required libraries.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install the required libraries:
        ```cmd
        pip install openai azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<deployment-name>
        set AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
        ```

=== "Linux/macOS"
    1. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    2. Install the required libraries:
        ```bash
        pip install openai azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/<deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

---

## 3. Main Code Components

### 3.1 OpenAI ChatCompletion Example

**Explanation:**  
This example uses the OpenAI Python SDK to get a chat completion. You provide the model name, messages, and your API key.

```python
import openai

openai.api_key = "<your-openai-api-key>"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"}
    ],
    temperature=0.7,
    max_tokens=50
)

print(response.choices[0].message["content"])
```

---

### 3.2 Azure Inference ChatCompletionsClient Example

**Explanation:**  
This example uses the Azure Inference SDK. The model is specified in the endpoint URL. You authenticate with an Azure key, and the message format is similar to OpenAI.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01"
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?")
    ],
    temperature=0.7,
    max_tokens=50
)

print(response.choices[0].message.content)
```

---

## 4. Complete Example: Azure Inference Chat Completion

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_OPENAI_CHAT_KEY"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01"
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?")
        ],
        temperature=0.7,
        max_tokens=50
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script authenticates with Azure, sends a chat completion request, and prints the assistant's response.

---

## 5. How to Run the Example

1. Ensure your environment variables are set as shown above.
2. Save the code to a file, for example, `azure_chat_completion.py`.
3. Run the script:
    ```bash
    python azure_chat_completion.py
    ```

---

## 6. Next Steps

- Review the [Azure AI Inference documentation](https://learn.microsoft.com/azure/ai-services/openai/reference){:target="_blank"} for advanced features.
- Explore structured output, function calling, and streaming responses.
- Update your code to use Azure-specific features as needed.

---

## Related Resources

- [Azure AI Inference Python SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat/create){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}