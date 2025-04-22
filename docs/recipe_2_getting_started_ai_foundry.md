# Deploy a New GPT-4o Model in Azure AI Foundry

This guide shows you how to deploy a new GPT-4o model in Azure AI Foundry. You will use the Azure AI Foundry portal to select, configure, and deploy the model for use in your applications.

## Prerequisites

- An Azure subscription with access to Azure AI Foundry.
- Contributor or Owner permissions on the Azure AI Foundry project.
- A project created in Azure AI Foundry.
- Sufficient quota for GPT-4o in your Azure region.
- Python 3.8+ and Azure AI Foundry services (if you plan to use the model programmatically).

## Introduction

GPT-4o is a state-of-the-art large language model available through Azure OpenAI Service. Deploying GPT-4o in Azure AI Foundry allows you to use it for chat, completions, and other generative AI scenarios. You can deploy the model using the Azure AI Foundry portal, and then access it via REST API or SDK.

## 1. Deploy GPT-4o Using the Azure AI Foundry Portal

1. **Sign in to the Azure AI Foundry portal**  
   Go to [https://ai.azure.com](https://ai.azure.com){:target="_blank"} and sign in with your Azure account.

2. **Select your project**  
   On the left navigation pane, select **Projects** and choose your project.

3. **Open the Model Catalog**  
   In your project, select **Model catalog** from the navigation menu.

4. **Search for GPT-4o**  
   Use the search bar to enter `gpt-4o`.  
   - You can also filter by **Provider**: Azure OpenAI, and **Deployment options**: Azure OpenAI.

5. **Select the GPT-4o model**  
   Click on the **GPT-4o** model card to open its details.

6. **Deploy the model**  
   - Click **Deploy**.
   - In the deployment form, provide:
     - **Deployment name**: Enter a unique name (e.g., `gpt-4o-deployment`).
     - **Model version**: Select the latest available version.
     - **Deployment type**: Choose **Azure OpenAI**.
     - **Quota**: Ensure you have sufficient quota for GPT-4o in your region.
   - Click **Deploy** to start the deployment.

7. **Monitor deployment status**  
   - Go to the **Deployments** tab in your project.
   - Wait for the deployment status to show **Succeeded**.

## 2. (Optional) Access the Deployed Model Programmatically

After deployment, you can use the model via REST API or SDK. The following example shows how to use the Python SDK.

### Environment Setup

Install the required Python libraries and set environment variables.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install required libraries:
        ```cmd
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
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
    2. Install required libraries:
        ```bash
        pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
        ```
    3. Set environment variables:
        ```bash
        export AZURE_OPENAI_CHAT_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        export AZURE_OPENAI_CHAT_KEY=<your-azure-openai-key>
        ```

## 3. Main Code Components

### a. Import Required Libraries

Import the Azure AI Inference client and message types.

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import os
```

### b. Set Up the Client

Create a client using your endpoint and key.

```python
endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
key = os.environ["AZURE_OPENAI_CHAT_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01",  # Use the latest supported API version
)
```

### c. Send a Chat Completion Request

Send a prompt to the deployed GPT-4o model.

```python
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How can I use GPT-4o in Azure AI Foundry?"),
    ]
)
print(response.choices[0].message.content)
```

## 4. Complete Example

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
            UserMessage("How can I use GPT-4o in Azure AI Foundry?"),
        ]
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

**Explanation:**  
This script sends a chat prompt to your deployed GPT-4o model and prints the response.

## 5. Run the Example Code

1. Ensure your environment variables are set.
2. Run the script:
    ```bash
    python <script-name>.py
    ```

## Next Steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Use GPT-4o for chat and completions](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt){:target="_blank"}
- [Manage deployments in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}