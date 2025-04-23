# Deploy a New GPT-4o Model in Azure AI Foundry

## Introduction

This guide explains how to deploy a new GPT-4o model in Azure AI Foundry. You will use the Azure AI Foundry portal to select, configure, and deploy the GPT-4o model for use in your applications. The goal is to make the model available as an endpoint for inference.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or later
- Access to Azure AI Foundry services
- Sufficient permissions in your Azure subscription to deploy models and create resources

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows"

    1. Open **Command Prompt** or **PowerShell**.
    2. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    3. Install required Python libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0 azure-storage-blob==12.25.1 azure-ai-projects==1.0.0b9
        ```
    4. Set environment variables. Replace the placeholders with the actual values:
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        set AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
        ```

=== "Linux/macOS"

    1. Open a terminal window.
    2. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    3. Install required Python libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0 azure-storage-blob==12.25.1 azure-ai-projects==1.0.0b9
        ```
    4. Set environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>"
        export AZURE_OPENAI_CHAT_KEY="<your-azure-openai-key>"
        ```

**Note:** Replace `<your-resource-name>`, `<your-deployment-name>`, and `<your-azure-openai-key>` with your actual Azure OpenAI resource and deployment details.

## 2. Main code components

### 2.1. Define the GPT-4o deployment endpoint

You need to specify the endpoint for your GPT-4o deployment. This is set using the `AZURE_OPENAI_CHAT_ENDPOINT` environment variable.

```python
import os

endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
```

### 2.2. Authenticate to Azure OpenAI

You can authenticate using an API key or Azure Entra ID. This example uses an API key.

```python
from azure.core.credentials import AzureKeyCredential

key = os.environ["AZURE_OPENAI_CHAT_KEY"]
credential = AzureKeyCredential(key)
```

### 2.3. Create the ChatCompletionsClient

This client is used to interact with the deployed GPT-4o model.

```python
from azure.ai.inference import ChatCompletionsClient

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=credential,
    api_version="2024-08-01-preview"  # Use the latest supported API version for GPT-4o
)
```

### 2.4. Send a test prompt to the deployed model

You can verify the deployment by sending a simple prompt.

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("What is new in GPT-4o?")
    ]
)
print(response.choices[0].message.content)
```

## 3. Complete code example

The following script demonstrates how to connect to your deployed GPT-4o model and send a prompt:

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
        print("Set them before running this script.")
        exit(1)

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-08-01-preview"
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("What is new in GPT-4o?")
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script authenticates to your Azure OpenAI GPT-4o deployment and sends a test prompt. The response from the model is printed to the console.

## 4. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the complete code example to a file, for example, `test_gpt4o_deployment.py`.
3. Run the script:

    ```bash
    python test_gpt4o_deployment.py
    ```

You should see the model's response printed in your terminal.

## 5. Next steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Deploy and manage models in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}
- [Azure AI Foundry Python SDK reference](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference){:target="_blank"}

For more advanced deployment options, such as managed compute or serverless APIs, refer to the Azure AI Foundry documentation.