# Deploy a New GPT-4o Model in Azure AI Foundry

## Introduction

This article explains how to deploy a new GPT-4o model in Azure AI Foundry. You will learn how to locate the model in the model catalog, configure deployment options, and complete the deployment process. The goal is to make the GPT-4o model available for inference in your Azure AI Foundry project.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- An Azure subscription with an Azure AI Foundry project created
- Sufficient permissions to deploy models in your project

## 1. Authentication

Azure AI Foundry supports several authentication methods for deploying and accessing models. You will need to authenticate to the Azure AI Foundry portal and, if using the SDK or CLI, provide credentials for your Azure subscription.

To authenticate:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"} with your Azure account.
2. Select your Azure AI Foundry project.
3. If using the SDK or CLI, authenticate using your Azure credentials (for example, with `az login`).

## 2. Developer environment setup

Select your preferred operating system and follow the steps below to prepare your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
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
    2. Create a project folder:
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

## 3. Deploy the GPT-4o Model

You can deploy the GPT-4o model using the Azure AI Foundry portal. The following steps guide you through the process:

1. Go to the [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"}.
2. Select your project from the list.
3. In the left navigation, select **Model catalog**.
4. Use the search bar or filters to find **GPT-4o**.
5. Select the **GPT-4o** model card to view details.
6. Click **Deploy**.
7. In the deployment form:
    - Enter a unique deployment name.
    - Select the deployment type (for GPT-4o, typically **Azure OpenAI**).
    - Choose the region and other configuration options as required.
    - Review pricing and terms.
8. Click **Deploy** to start the deployment process.
9. Wait for the deployment to complete. You can monitor the status in the **Deployments** or **Models + endpoints** tab.

After deployment, you will see the endpoint URL and key in the deployment details. Use these values to access the model for inference.

## 4. Main code components

The following code demonstrates how to verify your deployment by making a simple chat completion request to the deployed GPT-4o model.

### Import required libraries

This code imports the necessary libraries for authentication and making requests to the deployed model.

```python
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
```

### Create the client

This code creates a client for the deployed GPT-4o model using the endpoint and key.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Update if a newer API version is required
)
```

### Send a chat completion request

This code sends a simple prompt to the model and prints the response.

```python
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)

print(response.choices[0].message.content)
```

## 5. Complete code example

The following is a complete example. Save this code as `example.py`.

```python
"""
Example: Test your deployed GPT-4o model in Azure AI Foundry.

This script sends a simple prompt to your deployed GPT-4o model and prints the response.
Set the following environment variables before running:
- AZURE_OPENAI_CHAT_ENDPOINT: The endpoint URL of your deployment.
- AZURE_OPENAI_CHAT_KEY: The API key for your deployment.
"""

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    """
    Send a test prompt to the deployed GPT-4o model and print the response.
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
- [Azure AI Inference client library for Python documentation](https://aka.ms/aiservices/inference){:target="_blank"}
- [Deploy and manage models in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}
- [Samples for Azure AI Inference SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}
