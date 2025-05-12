# Introduction to Azure AI Foundry for Beginners

Azure AI Foundry is a platform that helps you discover, deploy, and use a wide range of AI models for your applications. It provides a unified experience for working with models from Microsoft, OpenAI, and other leading providers. Azure AI Foundry is designed to make it easy for you to organize your work, manage security, and control access to your AI resources.

## Introduction to Azure AI Foundry Components

Azure AI Foundry is built around several key components that help you manage and use AI models effectively:

### Hubs

A **Hub** is a top-level resource in Azure AI Foundry. It acts as a central point for managing security, networking, and access control for your AI resources. Hubs allow you to:

- Organize your AI resources across teams and projects.
- Set up network isolation and security policies.
- Control who can access and manage resources within the hub.

### Projects

A **Project** is a workspace within a hub where you can organize your AI assets, such as models, datasets, and deployments. Projects help you:

- Group related resources for a specific application or team.
- Manage access control at a more granular level.
- Track usage and billing for your AI workloads.

For more information, see [Explore foundation models in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}.

## Ways to Deploy Models in Azure AI Foundry

Azure AI Foundry offers several deployment options to suit different needs:

### 1. Serverless API (Pay-As-You-Go)

- **Preferred deployment method** for most users.
- Provides access to a wide range of models from various providers.
- Models are hosted and managed by Microsoft; you only pay for what you use (per token).
- No need to manage infrastructure.
- Fast and easy to get started.

Learn more: [Deploy models as serverless APIs](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless){:target="_blank"}

### 2. Managed Compute

- Allows you to deploy models to dedicated virtual machines managed by Azure.
- Often used for leading-edge models or early availability releases.
- Provides more control over compute resources and network isolation.
- Suitable for advanced scenarios or when you need custom configurations.

Learn more: [Deploy models with managed compute](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}

### 3. Azure OpenAI Service

- A managed service for OpenAI models (such as GPT-4, GPT-4o, etc.).
- Provides enterprise-grade security, compliance, and support.
- Integrates with Azure AI Foundry for unified management.

Learn more: [What is Azure OpenAI Service?](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}

## Authentication Methods for Accessing Models

To use models deployed in Azure AI Foundry, your applications need to authenticate. Azure AI Foundry supports several authentication methods:

### 1. Project Connection String

- Used to connect to an Azure AI Foundry project.
- The connection string is available in the **Overview** tab of your project in the Azure AI Foundry portal.
- Suitable for SDKs and tools that support project-based authentication.

Learn more: [Get the project connection string](https://learn.microsoft.com/azure/ai-foundry/how-to/project-connection-string){:target="_blank"}

### 2. API Key

- Used for authenticating directly to a model endpoint.
- API keys are available in the Azure AI Foundry portal under your model deployment's details.
- Commonly used for serverless API and Azure OpenAI Service deployments.

Learn more: [Manage API keys for Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/manage-keys){:target="_blank"}

### 3. Microsoft Entra ID (formerly Azure Active Directory)

- Provides secure, identity-based authentication for enterprise scenarios.
- Allows you to use role-based access control (RBAC) and integrate with your organization's identity provider.
- To enable Entra ID authentication, configure your deployment to allow it in the Azure AI Foundry portal.

Learn more: [Enable Microsoft Entra ID authentication](https://learn.microsoft.com/azure/ai-foundry/how-to/enable-entra-id-authentication){:target="_blank"}

## Where to Get Authentication Information

- **Project Connection String:**  
  Go to your project in the Azure AI Foundry portal. The connection string is shown on the **Overview** tab in the **Project details** section.

- **API Key:**  
  Go to your model deployment in the Azure AI Foundry portal. Under the **SDK** dropdown, select your preferred SDK and authentication type to view the key and endpoint.

- **Microsoft Entra ID:**  
  Enable Entra ID authentication in your deployment settings in the Azure AI Foundry portal. You may need to configure permissions and assign roles to users or applications.

## SDKs for Azure AI Foundry

Azure AI Foundry supports several SDKs to help you interact with models and deployments:

### Azure Inference SDK

- Unified SDK for accessing models deployed via serverless API or managed compute.
- Supports chat completions, embeddings, and more.
- Works with a wide range of models from different providers.

Learn more: [Azure AI Inference client library for Python](https://aka.ms/aiservices/inference){:target="_blank"}

### Azure OpenAI Service SDK

- Official SDK for working with Azure OpenAI Service models.
- Provides advanced features and full support for OpenAI models.

Learn more: [Azure OpenAI client library for Python](https://learn.microsoft.com/azure/ai-services/openai/quickstart-client-library){:target="_blank"}

## Simple Authentication Examples

Below are very simple Python examples for each authentication method. Replace the placeholders with your actual values.

### 1. Project Connection String

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="<PROJECT_CONNECTION_STRING>"
)
```

### 2. API Key

```python
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="<ENDPOINT_URL>",
    credential=AzureKeyCredential("<API_KEY>")
)
```

### 3. Microsoft Entra ID

```python
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="<ENDPOINT_URL>",
    credential=DefaultAzureCredential(),
    credential_scopes=["https://cognitiveservices.azure.com/.default"]
)
```

For more detailed examples and usage, see the [Azure AI Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"} and [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}.

---

**Next steps:**

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Deploy your first model](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless){:target="_blank"}
- [Get started with the Azure AI Inference SDK](https://aka.ms/aiservices/inference){:target="_blank"}
- [Learn about authentication in Azure](https://learn.microsoft.com/azure/ai-foundry/how-to/enable-entra-id-authentication){:target="_blank"}