# Deploy a New GPT-4o Model in Azure AI Foundry

## Introduction

This guide explains how to deploy a new GPT-4o model in Azure AI Foundry. You will use the Azure AI Foundry portal to select, configure, and deploy the GPT-4o model for inference. The goal is to make the model available for your applications through a managed endpoint.

## Prerequisites

- Python 3.8 or later (if you plan to use the model programmatically)
- Access to Azure AI Foundry services with sufficient permissions to deploy models
- An existing Azure AI Foundry project

## 1. Developer environment setup

Select your preferred operating system and follow the steps to prepare your environment if you plan to use the model programmatically.

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
    6. Set up environment variables:
        ```powershell
        $env:AZURE_OPENAI_CHAT_ENDPOINT="<your-endpoint-url>"
        $env:AZURE_OPENAI_CHAT_KEY="<your-api-key>"
        ```
        Replace the placeholders with the actual values from your Azure AI Foundry deployment.

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
    6. Set up environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT="<your-endpoint-url>"
        export AZURE_OPENAI_CHAT_KEY="<your-api-key>"
        ```
        Replace the placeholders with the actual values from your Azure AI Foundry deployment.

## 2. Deploy GPT-4o Model in Azure AI Foundry Portal

Follow these steps to deploy the GPT-4o model using the Azure AI Foundry portal:

1. Go to the [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"} and sign in.
2. Select your **Project** or create a new one.
3. In the left navigation, select **Model catalog**.
4. Use the search bar or filters to find **GPT-4o**.
5. Click the **GPT-4o** model card to open its details.
6. Select **Deploy**.
7. Choose the deployment option:
    - **Serverless API** (pay-per-token) or **Managed compute** (dedicated resources).
8. Configure deployment settings:
    - Enter a unique deployment name.
    - Select the region and compute size (if applicable).
    - Review and accept the license terms.
9. Click **Deploy**.
10. Wait for the deployment to complete. The portal will show the deployment status and endpoint details.

## 3. Main code components

After deployment, you can use the endpoint for inference. The following code components demonstrate how to call the deployed GPT-4o model using Python.

### 3.1. Import required libraries and set up the client

This component imports the necessary libraries and initializes the `ChatCompletionsClient` with your endpoint and credentials.

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
    api_version="2024-06-01",  # Use the API version that matches your deployment
)
```

### 3.2. Send a chat completion request

This component sends a prompt to the GPT-4o model and prints the response.

```python
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)

print(response.choices[0].message.content)
```

## 4. Complete code example

The following is a complete example that demonstrates how to call your deployed GPT-4o model. Save this code as `example.py`.

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
        print("Set them before running this sample.")
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

This script initializes the client, sends a prompt, and prints the model's response.

## 5. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Save the code as `example.py` in your project folder.
3. Run the script:

    ```bash
    python example.py
    ```

You should see the GPT-4o model's response printed in the terminal.

## 6. Next steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Deploy open models with Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}

For more advanced scenarios, such as structured output or integrating with other Azure services, refer to the Azure AI Foundry and Azure OpenAI documentation.