# 1. Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

This guide explains how to migrate your code from the OpenAI `ChatCompletion` API to the Azure Inference Chat Completion API. You will learn about parameter mapping, see code examples for both APIs, and understand the required environment setup.

## 2. Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 3. Parameter Mapping: OpenAI vs Azure Inference

The following table shows how common parameters in the OpenAI `ChatCompletion` API map to the Azure Inference API:

| OpenAI Parameter         | Azure Inference Parameter         | Notes                                                                 |
|--------------------------|-----------------------------------|-----------------------------------------------------------------------|
| `model`                  | Set in endpoint URL (deployment)  | Azure uses deployment name in the endpoint URL                        |
| `messages`               | `messages`                        | Both use a list of message objects                                    |
| `temperature`            | `temperature`                     | Same meaning                                                          |
| `top_p`                  | `top_p`                           | Same meaning                                                          |
| `max_tokens`             | `max_tokens`                      | Same meaning                                                          |
| `stop`                   | `stop`                            | Same meaning                                                          |
| `n`                      | `n`                               | Same meaning                                                          |
| `stream`                 | `stream`                          | Both support streaming                                                |
| `response_format`        | `response_format`                 | For structured output, use `JsonSchemaFormat` in Azure Inference      |
| `api_key`                | `AzureKeyCredential` or Entra ID  | Azure uses key or Entra ID authentication                             |
| `base_url`               | `endpoint`                        | Azure endpoint includes deployment path                               |

> For a full list of supported parameters, see the [Azure Inference documentation](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#key-concepts){:target="_blank"}.

## 4. Environment Setup

Set up your Python environment and required libraries.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install required libraries:
        ```cmd
        pip install openai==1.30.5 azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
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
    2. Install required libraries:
        ```bash
        pip install openai==1.30.5 azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<deployment-name>
        export AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
        ```

## 5. Main Code Components

### 5.1 OpenAI ChatCompletion Example

**Explanation:**  
This example uses the OpenAI Python SDK to send a chat completion request.

```python
import openai

openai.api_key = "<your-openai-api-key>"

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"},
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message.content)
```

### 5.2 Azure Inference Chat Completion Example

**Explanation:**  
This example uses the Azure Inference SDK to send a chat completion request to an Azure OpenAI deployment. The endpoint and key are read from environment variables.

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

## 6. Complete Code Example: Azure Inference

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
This script authenticates with Azure OpenAI using environment variables, sends a chat completion request, and prints the response.

## 7. How to Run the Example Code

1. Ensure your environment variables are set as shown in the setup section.
2. Save the code to a file, for example, `azure_inference_chat.py`.
3. Run the script:
    ```bash
    python azure_inference_chat.py
    ```

## 8. Next Steps

- [Azure AI Inference Python SDK documentation](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#key-concepts){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}
- [OpenAI Python Library documentation](https://platform.openai.com/docs/libraries/python-library){:target="_blank"}