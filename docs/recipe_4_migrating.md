# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

## Introduction

This guide explains how to migrate your code from the OpenAI `ChatCompletion` API to the Azure Inference Chat Completion API. You will learn about the differences in API parameters, how to set up your environment, and how to update your code to use Azure AI Foundry services for chat completions.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your development environment.

=== "Windows"

    1. Open **Command Prompt** or **PowerShell**.
    2. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    3. Install the required Python libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    4. Set the required environment variables:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        set AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
        ```
        Replace the placeholders with the actual values for your Azure OpenAI endpoint and key.

=== "Linux/macOS"

    1. Open a terminal.
    2. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    3. Install the required Python libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    4. Set the required environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        export AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
        ```
        Replace the placeholders with the actual values for your Azure OpenAI endpoint and key.

## 2. API Mapping

The following table maps the key parameters between the OpenAI `ChatCompletion` API and the Azure Inference Chat Completion API.

| OpenAI `ChatCompletion` Parameter | Azure Inference Parameter         | Notes                                                      |
|-----------------------------------|-----------------------------------|------------------------------------------------------------|
| `model`                          | Deployment in endpoint URL        | Azure uses deployment name in the endpoint URL              |
| `messages`                       | `messages`                        | Both use a list of message objects                         |
| `temperature`                    | `temperature`                     | Same parameter                                             |
| `max_tokens`                     | `max_tokens`                      | Same parameter                                             |
| `top_p`                          | `top_p`                           | Same parameter                                             |
| `stop`                           | `stop`                            | Same parameter                                             |
| `api_key`                        | `AZURE_OPENAI_CHAT_KEY`           | Set as environment variable or credential                  |
| `api_base`                       | `AZURE_OPENAI_CHAT_ENDPOINT`      | Set as environment variable or in client constructor       |
| `api_version`                    | `api_version`                     | Required for Azure Inference                               |
| `response_format`                | `response_format`                 | Supported in Azure for structured output                   |

## 3. Main code components

### 3.1 OpenAI Chat Completion Example

This code demonstrates how to use the OpenAI `ChatCompletion` API to get a chat response.

```python
import openai

openai.api_key = "<your-openai-api-key>"
openai.api_base = "https://api.openai.com/v1"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"},
    ],
    temperature=0.7,
    max_tokens=100,
    top_p=1,
    stop=None,
)

print(response.choices[0].message["content"])
```

**Explanation:**  
This code uses the OpenAI Python SDK to send a chat completion request. It specifies the model, messages, and optional parameters such as `temperature` and `max_tokens`.

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
    top_p=1,
    stop=None,
)

print(response.choices[0].message.content)
```

**Explanation:**  
This code uses the Azure AI Inference SDK to send a chat completion request. The endpoint and key are set via environment variables. The `messages` parameter uses `SystemMessage` and `UserMessage` objects.

## 4. Complete code example and explanation

Below is a complete example for Azure Inference Chat Completion. This code reads the endpoint and key from environment variables, creates a client, and sends a chat completion request.

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
        top_p=1,
        stop=None,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script initializes the Azure Inference client, sends a chat completion request, and prints the assistant's response.

## 5. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the code to a file, for example, `azure_inference_chat.py`.
3. Activate your virtual environment.
4. Run the script:
    ```bash
    python azure_inference_chat.py
    ```

## Next steps

- Review the [Azure AI Inference SDK documentation](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#key-concepts){:target="_blank"} for more advanced usage.
- Explore [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"} for more features and deployment options.
- Update your application logic to use Azure Inference for chat completions as shown above.