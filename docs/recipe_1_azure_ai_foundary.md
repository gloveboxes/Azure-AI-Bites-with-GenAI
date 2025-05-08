# Introduction to Azure AI Foundry and Its Components

## Introduction

Azure AI Foundry is a platform that helps you discover, deploy, and manage a wide range of AI models for your applications. It provides a unified experience for working with models from Microsoft, OpenAI, and other leading providers. Azure AI Foundry is designed to make it easy for you to organize your work, control access, and deploy models using different compute options.

This guide introduces the main components of Azure AI Foundry, explains the different ways to deploy models, describes authentication methods, and provides a simple example for each authentication type.

## Azure AI Foundry Components

Azure AI Foundry is organized around two main concepts: **Hubs** and **Projects**.

- **Hubs**: Hubs are the top-level containers in Azure AI Foundry. They provide a secure boundary for organizing your AI resources, managing network access, and applying security policies. Hubs help you control who can access your AI assets and how they are used.

- **Projects**: Projects are created within a hub and are used to group related AI resources, such as model deployments, data, and experiments. Projects make it easier to manage access control, track usage, and collaborate with others on specific AI solutions.

For more information, see [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}.

## Model Deployment Options in Azure AI Foundry

Azure AI Foundry offers several ways to deploy models, each suited to different needs:

- **Serverless API (Pay-as-you-go)**:  
  This is the preferred deployment option for most users. Serverless APIs allow you to access a wide range of models without managing infrastructure. You pay only for what you use, making it cost-effective and scalable. Many popular models are available for serverless deployment.

- **Managed Compute**:  
  Managed compute deployments are often used for leading-edge or early-availability models. With this option, models are deployed to dedicated virtual machines managed by Azure. This provides more control over the environment and is suitable for advanced scenarios.

- **Azure OpenAI Service**:  
  The Azure OpenAI Service is a managed service for deploying and using OpenAI models, such as GPT-4 and GPT-4o. It provides enterprise-grade security, compliance, and integration with other Azure services.

For more details, see [Model deployment options in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}.

## Authentication Methods for Accessing Models

When building applications that use models deployed in Azure AI Foundry, you need to authenticate your app. Azure AI Foundry supports several authentication methods:

- **Project Connection String**:  
  A project connection string is a unique string that provides access to a specific project in Azure AI Foundry. It is commonly used for SDKs and tools that need to connect to a project.  
  Learn more: [Project connection string documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/project-connection-string){:target="_blank"}

- **API Key**:  
  API keys are used to authenticate requests to model endpoints. You can generate and manage API keys in the Azure AI Foundry portal.  
  Learn more: [API key authentication](https://learn.microsoft.com/azure/ai-foundry/how-to/authentication-keys){:target="_blank"}

- **Microsoft Entra ID (formerly Azure Active Directory)**:  
  Microsoft Entra ID provides secure, identity-based authentication for enterprise applications. It is recommended for production scenarios where you need to manage access at scale.  
  Learn more: [Microsoft Entra ID authentication](https://learn.microsoft.com/azure/ai-foundry/how-to/authentication-entra-id){:target="_blank"}

## SDKs for Working with Azure AI Foundry

Azure AI Foundry supports multiple SDKs to help you integrate AI models into your applications:

- **Azure Inference SDK**:  
  The Azure Inference SDK is a Python library that provides a unified interface for accessing models deployed in Azure AI Foundry, including serverless and managed compute endpoints.  
  [Azure Inference SDK documentation](https://aka.ms/aiservices/inference){:target="_blank"}

- **Azure OpenAI Service SDK**:  
  The Azure OpenAI Service SDK is designed for working specifically with OpenAI models deployed in Azure. It provides features for chat completions, embeddings, and more.  
  [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}

## Simple Authentication Examples

Below are very simple Python examples for each authentication method. These examples use the Azure Inference SDK to send a prompt to a deployed model.

### 1. Project Connection String

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Set your project connection string as an environment variable
project_connection_string = os.environ["PROJECT_CONNECTION_STRING"]

# Authenticate using the project connection string
client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=project_connection_string
)

# Example: List agents in the project
agents = client.agents.list_agents()
print(agents)
```

### 2. API Key

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Set your endpoint and API key as environment variables
endpoint = os.environ["AZURE_AI_ENDPOINT"]
api_key = os.environ["AZURE_AI_KEY"]

# Authenticate using API key
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("How many feet are in a mile?"),
    ]
)
print(response.choices[0].message.content)
```

### 3. Microsoft Entra ID

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential

# Set your endpoint as an environment variable
endpoint = os.environ["AZURE_AI_ENDPOINT"]

# Authenticate using Microsoft Entra ID
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

## Next Steps

- Explore the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- Learn more about [model deployment options](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- Review [authentication methods](https://learn.microsoft.com/azure/ai-foundry/how-to/authentication-overview){:target="_blank"}
- Try the [Azure Inference SDK](https://aka.ms/aiservices/inference){:target="_blank"} and [Azure OpenAI Service SDK](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}