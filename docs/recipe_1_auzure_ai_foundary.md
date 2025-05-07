# Introduction to Azure AI Foundry and Its Components

## Introduction

Azure AI Foundry is a unified platform for discovering, deploying, and operationalizing AI models at scale. It provides a comprehensive environment for working with a wide range of AI models, including those from Microsoft, third-party providers, and open-source communities. Azure AI Foundry streamlines the process of deploying models, managing their lifecycle, and integrating them into applications using secure and scalable APIs.

This article introduces the core components of Azure AI Foundry, explains the different ways to deploy models, describes available authentication methods, and provides simple code examples for each authentication approach.

---

## 1. Azure AI Foundry and Its Components

### Azure AI Foundry

Azure AI Foundry is a platform that enables you to:

- Discover and evaluate a broad catalog of AI models from Microsoft, partners, and open-source providers.
- Deploy models as managed compute endpoints or serverless APIs.
- Manage the lifecycle of models, including updates, monitoring, and retirement.
- Integrate models into your applications using secure, scalable REST APIs.

For more information, see [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}.

### Azure Inference SDK

The Azure Inference SDK is a Python client library that allows you to interact with AI models deployed via Azure AI Foundry. With this SDK, you can:

- Authenticate and connect to model endpoints.
- Send inference requests (such as chat completions or embeddings).
- Retrieve model information and manage inference workflows.

For details, see [Azure AI Inference client library for Python](https://aka.ms/aiservices/inference){:target="_blank"}.

### Azure OpenAI Service

Azure OpenAI Service provides access to OpenAI’s powerful language models (such as GPT-4, GPT-3.5) hosted on Azure. It offers:

- Enterprise-grade security, compliance, and regional availability.
- Integration with Azure AI Foundry for deployment and management.
- REST APIs and SDKs for easy integration into your applications.

Learn more at [What is Azure OpenAI Service?](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}.

---

## 2. Model Deployment Options in Azure AI Foundry

Azure AI Foundry supports multiple deployment options to meet different operational and cost requirements:

- **Managed Compute Endpoints**:  
  Deploy models to dedicated, scalable virtual machines managed by Azure. This option provides full control over compute resources, network isolation, and advanced configuration. You are billed for the compute resources used.

- **Serverless API Endpoints (Pay-per-token)**:  
  Deploy models as serverless APIs hosted in Microsoft-managed infrastructure. This option offers simplified deployment, automatic scaling, and pay-as-you-go billing based on usage (typically per token). It is ideal for rapid prototyping and production workloads without infrastructure management.

- **Azure OpenAI Service Endpoints**:  
  Deploy and access OpenAI models through Azure OpenAI Service, with support for both managed compute and serverless options, depending on the model and region.

For more details, see [Model catalog and collections in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview#model-deployment-managed-compute-and-serverless-apis){:target="_blank"}.

---

## 3. Authentication Methods for Accessing Models in Azure AI Foundry

Azure AI Foundry supports several authentication methods for applications to securely access deployed models:

- **API Key Authentication**:  
  Use a secret key provided by Azure AI Foundry or Azure OpenAI Service. This is the most common method for serverless API and managed compute endpoints.

- **Microsoft Entra ID (formerly Azure Active Directory) Authentication**:  
  Use Microsoft Entra ID credentials (such as service principals or managed identities) to authenticate securely without managing secrets. This is supported for managed compute endpoints and Azure OpenAI Service.

- **Project Connection String**:  
  Use a connection string to connect to an Azure AI Foundry project, typically for project-level operations and management.

Each method provides different levels of security and integration flexibility, depending on your application’s requirements.

---

## 4. Simple Authentication Examples

Below are minimal Python examples for each authentication method using the Azure AI Inference SDK.

### Prerequisites

- Python 3.8+
- Required Python libraries:
  - `azure-ai-inference==1.0.0b9`
  - `azure-core==1.33.0`
  - `azure-identity==1.21.0` (for Entra ID authentication)

Install the required libraries:

```bash
pip install azure-ai-inference==1.0.0b9 azure-core==1.33.0 azure-identity==1.21.0
```

### 4.1. API Key Authentication

This method uses an API key to authenticate with a model endpoint.

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Replace with your endpoint and key
endpoint = "https://<your-endpoint>.models.ai.azure.com"
key = "<your-api-key>"

client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)

print(response.choices[0].message.content)
```

### 4.2. Microsoft Entra ID Authentication

This method uses Microsoft Entra ID credentials for secure authentication.

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential

# Replace with your endpoint
endpoint = "https://<your-endpoint>.models.ai.azure.com"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False)
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)

print(response.choices[0].message.content)
```

### 4.3. Project Connection String

This method is used for project-level operations with Azure AI Foundry.

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Replace with your project connection string
project_connection_string = "<your-project-connection-string>"

client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=project_connection_string
)

# Example: List agents in the project
agents = client.agents.list_agents()
print(agents)
```

---

## Next Steps

- Explore the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}.
- Review the [Azure AI Inference SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples){:target="_blank"}.
- Learn more about [authentication in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/security-authentication){:target="_blank"}.
- Try deploying and testing models using the [Azure AI Foundry portal](https://ai.azure.com/){:target="_blank"}.

For more advanced scenarios, refer to the official documentation and SDK reference guides.