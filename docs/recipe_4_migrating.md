# Migrate from OpenAI Chat Completion to Azure Inference Chat Completion

This guide helps you migrate your code from the OpenAI Python SDK's `ChatCompletion` API to the Azure Inference SDK's `ChatCompletionsClient`. You will find a parameter mapping table, code examples for both APIs, and step-by-step migration instructions.

---

## 1. Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- An Azure OpenAI deployment and endpoint

---

## 2. Parameter Mapping: OpenAI vs Azure Inference

| OpenAI `openai.ChatCompletion.create` | Azure Inference `ChatCompletionsClient.complete` | Notes |
|---------------------------------------|--------------------------------------------------|-------|
| `model`                              | *Deployment is set in endpoint URL*              | Azure uses deployment in endpoint, not as a parameter |
| `messages`                           | `messages`                                       | Same format (list of message objects) |
| `temperature`                        | `temperature`                                    | Same meaning |
| `max_tokens`                         | `max_tokens`                                     | Same meaning |
| `top_p`                              | `top_p`                                          | Same meaning |
| `stop`                               | `stop`                                           | Same meaning |
| `n`                                  | `n`                                              | Same meaning |
| `stream`                             | `stream`                                         | Same meaning |
| `presence_penalty`                   | `presence_penalty`                               | Same meaning |
| `frequency_penalty`                  | `frequency_penalty`                              | Same meaning |
| `logit_bias`                         | `logit_bias`                                     | Same meaning |
| `user`                               | `user`                                           | Same meaning |
| `api_key`                            | `credential=AzureKeyCredential(key)`             | Use AzureKeyCredential or Azure Identity |
| `api_base`                           | `endpoint`                                       | Azure endpoint includes deployment path |
| `api_version`                        | `api_version`                                    | Must be specified for Azure |

---

## 3. Example: OpenAI Chat Completion

```python
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_base = "https://api.openai.com/v1"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many feet are in a mile?"}
    ],
    temperature=0.7,
    max_tokens=50,
    n=1,
    stop=None,
)

print(response.choices[0].message["content"])
```

---

## 4. Example: Azure Inference Chat Completion

### 4.1. Set Up Python Virtual Environment and Environment Variables

#### Windows

1. Open **Command Prompt**.
2. Create and activate a virtual environment:
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```
3. Install required libraries:
    ```cmd
    pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
    ```
4. Set environment variables:
    ```cmd
    set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>
    set AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
    ```

#### Linux/macOS

1. Open **Terminal**.
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install required libraries:
    ```bash
    pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0
    ```
4. Set environment variables:
    ```bash
    export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>"
    export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
    ```

---

### 4.2. Main Code Components

- **Import Libraries**: Import Azure Inference SDK and credentials.
- **Read Environment Variables**: Get endpoint and key.
- **Create Client**: Use `ChatCompletionsClient` with endpoint and credentials.
- **Send Messages**: Use `SystemMessage` and `UserMessage` for the conversation.
- **Get and Print Response**: Access the response content.

---

### 4.3. Complete Azure Inference Example

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
        api_version="2024-06-01",  # Use the latest supported API version
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ],
        temperature=0.7,
        max_tokens=50,
        n=1,
        stop=None,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

---

### 4.4. How to Run the Example

1. Ensure your environment variables are set as described above.
2. Run the script:
    ```bash
    python your_script_name.py
    ```

---

## 5. Next Steps

- [Azure AI Inference Python SDK documentation](https://learn.microsoft.com/python/api/overview/azure/ai-inference-readme){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/){:target="_blank"}
- [OpenAI Python Library documentation](https://platform.openai.com/docs/libraries/python-library){:target="_blank"}

---

By following this guide, you can migrate your OpenAI ChatCompletion code to use Azure Inference with minimal changes. Adjust parameters as needed for your specific use case.