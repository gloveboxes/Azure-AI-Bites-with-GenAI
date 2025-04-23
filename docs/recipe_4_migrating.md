# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This guide explains how to migrate your application from the OpenAI `ChatCompletion` API to the Azure Inference Chat Completion API. You will learn about the differences in API parameters, see code examples for both services, and understand how to update your code for Azure AI Foundry services.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system to set up your development environment.

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
        set AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
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
        export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

## 2. API Mapping

The following table maps the key parameters between the OpenAI `ChatCompletion` API and the Azure Inference Chat Completion API.

| OpenAI `ChatCompletion` Parameter | Azure Inference Parameter         | Notes                                                      |
|-----------------------------------|-----------------------------------|------------------------------------------------------------|
| `model`                          | Set in endpoint URL               | Azure uses deployment name in the endpoint URL              |
| `messages`                       | `messages`                        | Same structure (list of message objects)                   |
| `temperature`                    | `temperature`                     | Supported                                                  |
| `max_tokens`                     | `max_tokens`                      | Supported                                                  |
| `top_p`                          | `top_p`                           | Supported                                                  |
| `n`                              | `n`                               | Supported                                                  |
| `stop`                           | `stop`                            | Supported                                                  |
| `stream`                         | `stream`                          | Supported                                                  |
| `presence_penalty`               | `presence_penalty`                | Supported                                                  |
| `frequency_penalty`              | `frequency_penalty`               | Supported                                                  |
| `logit_bias`                     | `logit_bias`                      | Supported                                                  |
| `user`                           | `user`                            | Supported                                                  |
| `functions`                      | `functions`                       | Supported (for function calling)                           |
| `function_call`                  | `function_call`                   | Supported                                                  |
| `response_format`                | `response_format`                 | Supported (for structured output, e.g., JSON schema)       |
| `api_key`                        | `credential` (AzureKeyCredential) | Use AzureKeyCredential or DefaultAzureCredential           |
| `api_base`                       | `endpoint`                        | Use full Azure endpoint with deployment path               |
| `api_version`                    | `api_version`                     | Required for Azure Inference                               |

## 3. Main code components

### 3.1 OpenAI Chat Completion Example

This code demonstrates how to use the OpenAI `ChatCompletion` API to get a chat response.

```python
import openai

openai.api_key = "<your-openai-api-key>"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"},
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message["content"])
```

**Explanation:**  
This code uses the OpenAI Python SDK to send a chat completion request. You specify the model, messages, and optional parameters such as `temperature` and `max_tokens`.

---

### 3.2 Azure Inference Chat Completion Example

This code demonstrates how to use the Azure Inference Chat Completion API to get a chat response.

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
    api_version="2024-06-01",
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message.content)
```

**Explanation:**  
This code uses the Azure Inference SDK to send a chat completion request. The endpoint includes the deployment name, and authentication uses `AzureKeyCredential`. The message structure and parameters are similar to OpenAI.

---

## 4. Complete code example

Below is a complete example for Azure Inference Chat Completion, including environment variable handling.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    try:
        endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_OPENAI_CHAT_KEY"]
    except KeyError:
        print("Please set AZURE_OPENAI_CHAT_ENDPOINT and AZURE_OPENAI_CHAT_KEY environment variables.")
        return

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01",
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ],
        temperature=0.7,
        max_tokens=100,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script reads the required environment variables, initializes the Azure Inference client, sends a chat completion request, and prints the response.

---

## 5. How to run the example code

1. Set up your environment as described in the **Developer environment setup** section.
2. Save the complete code example to a file, for example, `azure_inference_chat.py`.
3. Run the script:
    ```bash
    python azure_inference_chat.py
    ```

---

## 6. Next steps

- Review the [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#key-concepts){:target="_blank"}.
- Explore advanced features such as function calling and structured output.
- Learn more about [Azure AI Foundry model catalog](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}.

---

**Related resources:**

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat){:target="_blank"}
- [Azure AI Inference API Reference](https://learn.microsoft.com/python/api/overview/azure/ai-inference-readme){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}