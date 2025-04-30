# Deploy a New GPT-4o Model in Azure AI Foundry

## Introduction

This article explains how to deploy a new GPT-4o model in Azure AI Foundry. You will learn how to select the model from the catalog, configure deployment options, and access the endpoint for inference.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- An Azure subscription with the necessary permissions to create deployments

## 1. Authentication

Azure AI Foundry supports several authentication methods for deploying and accessing models. You will need to authenticate to the Azure AI Foundry portal and, if using the SDK, provide credentials for API access.

**Azure AI Foundry** is a platform for discovering, deploying, and managing AI models, including GPT-4o, from a unified catalog. It supports both managed compute and serverless API deployment options.

To authenticate:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"} with your Azure account.
2. Ensure you have access to a project and the required permissions to deploy models.
3. If using the SDK, obtain your **Project Connection String** or **API Key** from the portal.

## 2. Developer environment setup

Select your preferred operating system:

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir my-gpt4o-deployment
        cd my-gpt4o-deployment
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
    6. Set up environment variables:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="<your-gpt4o-endpoint>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-api-key>"
        ```
        Replace the placeholders with the actual values from the Azure AI Foundry portal.

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir my-gpt4o-deployment
        cd my-gpt4o-deployment
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
    6. Set up environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="<your-gpt4o-endpoint>"
        export AZURE_OPENAI_CHAT_KEY="<your-api-key>"
        ```
        Replace the placeholders with the actual values from the Azure AI Foundry portal.

## 3. Deploy the GPT-4o Model

### Step 1: Select the GPT-4o Model

1. Go to the [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"}.
2. Navigate to the **Model Catalog**.
3. Search for **GPT-4o**.
4. Select the GPT-4o model card.

### Step 2: Configure Deployment

1. Click **Deploy** on the model card.
2. Choose your deployment option:
    - **Serverless API** (pay-per-token, managed by Microsoft)
    - **Managed Compute** (deployed to your own Azure resources)
3. Select your **Azure AI Foundry project** and configure deployment settings:
    - Deployment name
    - Region
    - Quota (if using managed compute)
    - Any additional settings as required

4. Review and accept the license terms.
5. Click **Deploy**.

The deployment process may take a few minutes. Once complete, you will see the deployment listed under **Existing deployments** on the model card.

### Step 3: Retrieve Endpoint and Key

1. In your project, go to the **Models + endpoints** tab.
2. Find your GPT-4o deployment.
3. Click on the deployment to view details.
4. Copy the **Endpoint URL** and **API Key** for use in your applications.

## 4. Main code components

Below is a sample Python script to verify your deployment by making a chat completion request to the GPT-4o endpoint.

### Import required libraries

This code imports the necessary libraries for authentication and making requests to the deployed model.

```python
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
```

### Create the client and send a request

This code creates a client using your endpoint and key, then sends a chat completion request.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

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

## 5. Complete code example

The following script demonstrates how to connect to your deployed GPT-4o model and get a response. Save this as `example.py`.

```python
"""
Example: Connect to a deployed GPT-4o model in Azure AI Foundry and get a chat completion response.

Set the following environment variables before running:
- AZURE_OPENAI_CHAT_ENDPOINT: The endpoint URL for your GPT-4o deployment.
- AZURE_OPENAI_CHAT_KEY: The API key for your deployment.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Connects to the GPT-4o deployment and sends a chat completion request.
    """
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
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

## 6. How to run the example code

1. Ensure your environment variables are set as described in the developer environment setup.
2. Save the code above as `example.py`.
3. Run the script:

    ```bash
    python example.py
    ```

You should see the model's response printed in the terminal.

## 7. Next steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure AI Inference Python SDK documentation](https://aka.ms/azsdk/azure-ai-inference/python/reference){:target="_blank"}
- [Deploy and manage models in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}