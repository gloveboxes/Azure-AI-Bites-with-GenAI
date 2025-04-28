# Deploy a New GPT-4o Model in Azure AI Foundry

## Introduction

This guide explains how to deploy a new GPT-4o model in Azure AI Foundry. You will use the Azure AI Foundry portal to select, configure, and deploy the GPT-4o model for inference. The goal is to make the model available for your applications through a managed endpoint.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- Sufficient permissions in your Azure subscription to deploy models

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open **PowerShell**.
    2. Create a new project folder:
        ```powershell
        mkdir gpt4o-deployment
        cd gpt4o-deployment
        ```
    3. Set up a virtual environment:
        ```powershell
        python -m venv .venv
        ```
    4. Activate the virtual environment:
        ```powershell
        .\.venv\Scripts\Activate
        ```
    5. Install the required libraries:
        ```powershell
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a new project folder:
        ```bash
        mkdir gpt4o-deployment
        cd gpt4o-deployment
        ```
    3. Set up a virtual environment:
        ```bash
        python3 -m venv .venv
        ```
    4. Activate the virtual environment:
        ```bash
        source .venv/bin/activate
        ```
    5. Install the required libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

## 2. Main code components

### 2.1. Import required libraries and set up the client

This section imports the necessary libraries and sets up the `ChatCompletionsClient` to interact with the deployed GPT-4o model.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
```

### 2.2. Configure environment variables

This code retrieves the endpoint and key from environment variables. It ensures the required values are set before proceeding.

```python
try:
    endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_OPENAI_CHAT_KEY"]
except KeyError:
    print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT' or 'AZURE_OPENAI_CHAT_KEY'")
    exit()
```

### 2.3. Create the client and send a test request

This code creates the client and sends a sample chat completion request to verify the deployment.

```python
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the latest supported API version for GPT-4o
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)

print(response.choices[0].message.content)
```

## 3. Complete code example

The following is the complete code to test your GPT-4o deployment. Save this as `example.py`.

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
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT' or 'AZURE_OPENAI_CHAT_KEY'")
        exit()

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-06-01",
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

This script sends a test prompt to your deployed GPT-4o model and prints the response.

## 4. How to run the example code

1. Ensure your virtual environment is activated and environment variables are set.
2. Run the script:
    ```bash
    python example.py
    ```
3. You should see the model's response printed in the terminal.

## 5. Next steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Deploy and manage models in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}

For advanced scenarios, such as structured output or integrating with other Azure services, refer to the Azure AI Foundry and Azure OpenAI documentation.