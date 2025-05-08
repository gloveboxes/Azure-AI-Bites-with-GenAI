# Introduction to Azure AI Foundry for Beginners

Azure AI Foundry is a platform that helps you discover, deploy, and use a wide range of AI models for your applications. This guide introduces the main components of Azure AI Foundry, explains how to organize your work, describes model deployment options, and shows how to authenticate your applications. It also provides a brief overview of available SDKs and simple code examples for each authentication method.

---

## 1. What is Azure AI Foundry?

Azure AI Foundry is a unified platform for working with AI models from Microsoft and leading partners. It enables you to:

- Explore a catalog of foundation models and open models.
- Deploy models using different compute options.
- Securely manage access and organize your work.
- Integrate models into your applications using SDKs and APIs.

Azure AI Foundry is designed to make it easy for both beginners and experienced developers to build generative AI solutions.

---

## 2. Organizing Your Work: Hubs and Projects

Azure AI Foundry uses **Hubs** and **Projects** to help you organize, secure, and manage your AI resources.

- **Hubs**: A hub is a top-level resource that provides a secure boundary for your AI assets. It controls network access, security policies, and resource sharing across projects.
- **Projects**: Projects are containers within a hub where you manage your model deployments, data, and application resources. Projects help you group related work, manage access control, and collaborate with others.

:::image type="content" source="../media/explore/platform-service-cycle.png" alt-text="Diagram that shows models as a service and the service cycle of managed computes." lightbox="../media/explore/platform-service-cycle.png":::

For more details, see [Model catalog and collections in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}.

---

## 3. Model Deployment Options in Azure AI Foundry

Azure AI Foundry offers several ways to deploy and use AI models:

### Serverless API (Pay-As-You-Go)

- **Preferred for most users.**
- Deploy models as serverless APIs with pay-per-token billing.
- No need to manage infrastructure.
- Wide range of models available from Microsoft and partners.
- Fast and easy to get started.

### Managed Compute

- Deploy models to dedicated virtual machines managed by Azure.
- Often used for leading-edge or early-availability models.
- Provides more control over compute resources and network isolation.
- Requires managing quotas and compute resources.

### Azure OpenAI Service

- Managed service for OpenAI models (such as GPT-4, GPT-4o).
- Integrated with Azure security, compliance, and monitoring.
- Supports both key and Microsoft Entra ID authentication.

For a detailed comparison, see [Model catalog and collections in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview#capabilities-of-model-deployment-options){:target="_blank"}.

---

## 4. Authentication Methods for Accessing Models

When your application accesses a model deployed in Azure AI Foundry, you must authenticate using one of the following methods:

### Project Connection String

- Used to connect to a specific Azure AI Foundry project.
- Contains all necessary information (endpoint, credentials) in a single string.
- Easy to use for development and automation.

### API Key

- A secret key associated with a model deployment or endpoint.
- Simple to use and widely supported.
- Keep your API keys secure and do not share them publicly.

### Microsoft Entra ID (formerly Azure Active Directory)

- Enterprise-grade identity and access management.
- Supports role-based access control and conditional access policies.
- Recommended for production and multi-user scenarios.

For more information, see [Azure AI Foundry authentication documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview#api-authentication){:target="_blank"}.

---

## 5. SDKs for Working with Azure AI Foundry

Azure AI Foundry supports several SDKs to help you integrate models into your applications:

- **Azure Inference SDK**: Unified SDK for accessing models deployed via serverless API or managed compute. Supports chat completions, embeddings, and more.
  - [Azure AI Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}
- **Azure OpenAI Service SDK**: Official SDK for working with OpenAI models deployed in Azure.
  - [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}

You can install the Azure Inference SDK using:

```bash
pip install azure-ai-inference
```

---

## 6. Simple Authentication Examples

Below are minimal Python examples for each authentication method using the Azure Inference SDK.

### Prerequisites

- Python 3.8 or later
- [azure-ai-inference](https://pypi.org/project/azure-ai-inference/){:target="_blank"} version 1.0.0b9
- [azure-core](https://pypi.org/project/azure-core/){:target="_blank"} version 1.33.0
- [azure-identity](https://pypi.org/project/azure-identity/){:target="_blank"} version 1.21.0 (for Entra ID)

### Example 1: Using Project Connection String

```python
from azure.ai.inference import load_client
from azure.core.credentials import AzureKeyCredential

# Replace with your actual project connection string
project_connection_string = "<your_project_connection_string>"

client = load_client(
    endpoint=project_connection_string,
    credential=AzureKeyCredential("<your_api_key>")
)

response = client.complete(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I get started with Azure AI Foundry?"}
    ]
)
print(response.choices[0].message.content)
```

### Example 2: Using API Key

```python
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "<your_model_endpoint>"
api_key = "<your_api_key>"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)

response = client.complete(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Azure AI Foundry?"}
    ]
)
print(response.choices[0].message.content)
```

### Example 3: Using Microsoft Entra ID

```python
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

endpoint = "<your_model_endpoint>"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False)
)

response = client.complete(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I use Entra ID with Azure AI Foundry?"}
    ]
)
print(response.choices[0].message.content)
```

> **Note:** Replace the placeholder values (such as `<your_model_endpoint>`, `<your_api_key>`, and `<your_project_connection_string>`) with your actual values from the Azure AI Foundry portal.

---

## Next Steps

- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Deploy models in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-managed){:target="_blank"}
- [Azure AI Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}

---

By following this guide, you can get started with Azure AI Foundry, deploy models, and integrate them into your applications using the authentication method that best fits your needs.