# Introduction to Azure AI Foundry and Its Components

## Introduction

Azure AI Foundry is a platform that helps you discover, deploy, and use a wide range of AI models for building generative AI applications. It brings together model management, deployment, and inference capabilities in a unified environment. This guide introduces the main components of Azure AI Foundry, explains how to deploy models, describes the concepts of hubs and projects, and provides an overview of authentication methods with simple examples.

---

## 1. What is Azure AI Foundry?

Azure AI Foundry is a cloud-based platform that enables you to:

- Explore a catalog of foundation models from Microsoft and leading partners.
- Deploy models using different compute options.
- Manage and monitor your AI resources.
- Build and run AI-powered applications securely and at scale.

Azure AI Foundry is designed to simplify the process of working with AI models, whether you are a beginner or an experienced developer.

[](/media/explore/platform-service-cycle.png){:target="_blank"}

*Diagram: Models as a service and the service cycle of managed computes in Azure AI Foundry.*

---

## 2. Key Components of Azure AI Foundry

### Azure Inference SDK

The Azure Inference SDK is a Python library that allows you to interact with AI models deployed in Azure AI Foundry. You can use it to:

- Authenticate against the service.
- Get information about deployed models.
- Run chat completions, text embeddings, and image embeddings.

[Learn more about the Azure Inference SDK](https://aka.ms/aiservices/inference){:target="_blank"}

### Azure OpenAI Service

Azure OpenAI Service provides access to OpenAI’s powerful language models, such as GPT-4, hosted on Azure. You can deploy and use these models through Azure AI Foundry, benefiting from Azure’s security, compliance, and enterprise features.

[Learn more about Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}

---

## 3. Ways to Deploy Models in Azure AI Foundry

Azure AI Foundry offers several deployment options for models:

| Deployment Option         | Description                                                                 | Billing Model         | Authentication         |
|--------------------------|-----------------------------------------------------------------------------|----------------------|------------------------|
| **Serverless API**       | Preferred. Deploy models as APIs managed by Microsoft. No infrastructure to manage. | Pay-as-you-go (per token) | API Key only           |
| **Managed Compute**      | Deploy models to dedicated virtual machines in your subscription.            | VM core hours         | API Key or Entra ID    |
| **Azure OpenAI Service** | Deploy OpenAI models with Azure integration.                                 | Pay-as-you-go         | API Key or Entra ID    |

**Preferred deployment:** Serverless API (pay-as-you-go) is recommended for most users because it is simple, scalable, and requires no infrastructure management.

[](/media/explore/model-publisher-cycle.png){:target="_blank"}

*Diagram: Model publisher service cycle for serverless API deployments.*

---

## 4. Hubs and Projects

Azure AI Foundry organizes resources using two main concepts:

- **Hubs:** A hub is a central resource that manages networking, security, and access policies for your AI workloads. It acts as a container for one or more projects.
- **Projects:** A project is a workspace within a hub where you deploy, manage, and use AI models. Projects help you organize models, deployments, and related assets for specific applications or teams.

---

## 5. Authentication Methods

To access models deployed in Azure AI Foundry from your applications, you need to authenticate. The main authentication methods are:

| Authentication Method | Description                                                                 | Supported Deployments         |
|----------------------|-----------------------------------------------------------------------------|------------------------------|
| **API Key**          | Use a secret key provided by Azure to authenticate requests.                 | Serverless API, Managed Compute, Azure OpenAI |
| **Microsoft Entra ID (formerly Azure AD)** | Use your Microsoft Entra (Azure AD) identity for secure, role-based access. | Managed Compute, Azure OpenAI |

---

## 6. Simple Authentication Examples

Below are minimal Python examples for each authentication method using the Azure Inference SDK.

### Prerequisites

- Python 3.8+
- Azure AI Foundry services (with a deployed model)
- [Install the Azure Inference SDK](https://aka.ms/aiservices/inference){:target="_blank"}

### Example 1: API Key Authentication (Serverless API or Managed Compute)

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

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

### Example 2: Microsoft Entra ID Authentication (Managed Compute or Azure OpenAI)

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential

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

### Example 3: API Key Authentication (Azure OpenAI Service)

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>"
key = "<your-aoai-key>"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    api_version="2024-06-01"
)
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)
print(response.choices[0].message.content)
```

---

## Next Steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Deploy models using managed compute](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}
- [Learn about authentication in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/authentication){:target="_blank"}
- [Azure AI Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}

---

By understanding these basics, you can start exploring, deploying, and using AI models in Azure AI Foundry with confidence.