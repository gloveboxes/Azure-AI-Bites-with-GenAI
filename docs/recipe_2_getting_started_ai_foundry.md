# Deploy a New GPT-4o Model in Azure AI Foundry

## Introduction

This guide explains how to deploy a new GPT-4o model in Azure AI Foundry. You will use the Azure AI Foundry portal to select, configure, and deploy the GPT-4o model for your project. After deployment, you can use the model for inference in your applications.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or later.
- Access to Azure AI Foundry services.
- Sufficient permissions in your Azure subscription to create and manage resources in Azure AI Foundry.

## 1. Deploy GPT-4o Model Using Azure AI Foundry Portal

Follow these steps to deploy the GPT-4o model:

1. **Sign in to Azure AI Foundry Portal**
   - Go to [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"}.
   - Sign in with your Azure account.

2. **Create or Select a Project**
   - In the portal, select an existing project or create a new one by selecting **New project** and following the prompts.

3. **Open the Model Catalog**
   - In your project, navigate to the **Model catalog** from the left navigation pane.

4. **Search for GPT-4o**
   - Use the search bar to enter `gpt-4o`.
   - Locate the **GPT-4o** model from the search results.

5. **Review Model Details**
   - Select the GPT-4o model card to view details, including supported deployment options, pricing, and documentation.

6. **Deploy the Model**
   - Click **Deploy**.
   - Choose your deployment option:
     - **Azure OpenAI** (recommended for GPT-4o).
     - **Managed Compute** or **Serverless API** (if available).
   - Configure deployment settings:
     - **Deployment name**: Enter a unique name.
     - **Region**: Select the Azure region.
     - **Scale settings**: Choose the compute size and scaling options.
   - Review and accept the license terms.
   - Click **Deploy** to start the deployment process.

7. **Monitor Deployment Status**
   - Go to the **Deployments** tab in your project to monitor the deployment status.
   - Wait until the status changes to **Succeeded**.

8. **Get Endpoint and Keys**
   - After deployment, select your deployment to view details.
   - Copy the **Endpoint URL** and **API key** for use in your applications.

## 2. Developer Environment Setup

Select your preferred operating system tab and follow the steps to set up your environment for using the deployed GPT-4o model.

Select your preferred operating system:

=== "Windows"

    1. Open **Command Prompt**.
    2. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    3. Install required Python libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    4. Set environment variables (replace *<your_value>* with your actual values):
        ```cmd
        set AZURE_OPENAI_CHAT_ENDPOINT=<your_endpoint_url>
        set AZURE_OPENAI_CHAT_KEY=<your_api_key>
        ```

=== "Linux/macOS"

    1. Open **Terminal**.
    2. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    3. Install required Python libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    4. Set environment variables (replace *<your_value>* with your actual values):
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=<your_endpoint_url>
        export AZURE_OPENAI_CHAT_KEY=<your_api_key>
        ```

## 3. Main Code Components

Below are the main components for using your deployed GPT-4o model for chat completions.

### 3.1. Import Required Libraries

You need to import the Azure AI Inference client and message types.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
```

### 3.2. Set Up the Client

Create a client instance using your endpoint and API key.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the API version that matches your deployment
)
```

### 3.3. Send a Chat Completion Request

Prepare your messages and send a request to the GPT-4o model.

```python
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)
```

### 3.4. Process the Response

Extract and print the model's response.

```python
print(response.choices[0].message.content)
```

## 4. Complete Code Example

This example demonstrates how to connect to your deployed GPT-4o model and get a chat completion.

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
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script authenticates to your deployed GPT-4o model using the endpoint and API key, sends a simple chat prompt, and prints the model's response.

## 5. How to Run the Example Code

1. Ensure your environment variables are set as described in the setup section.
2. Save the complete code example to a file, for example, `chat_gpt4o_example.py`.
3. Run the script:
    ```bash
    python chat_gpt4o_example.py
    ```
4. You should see the model's response printed in your terminal.

## Next Steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Build generative AI apps with Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}