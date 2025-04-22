# Deploy a New GPT-4o Model in Azure AI Foundry

This guide shows you how to deploy a new GPT-4o model in Azure AI Foundry. You will use the Azure AI Foundry portal to create a deployment, making the model available for inference in your projects.

## Prerequisites

- Access to an [Azure AI Foundry](https://ai.azure.com){:target="_blank"} workspace with **Project Contributor** or higher permissions.
- An active Azure subscription.
- The GPT-4o model available in your region and project.
- Python 3.8+ and Azure AI Foundry services (for code-based deployment or testing).

## Introduction

GPT-4o is a state-of-the-art large language model available through Azure OpenAI Service and Azure AI Foundry. Deploying GPT-4o in Azure AI Foundry allows you to use the model for generative AI applications, including chat, summarization, and more.

You can deploy GPT-4o using the Azure AI Foundry portal or programmatically. This article focuses on the portal experience, with a note on programmatic deployment.

---

## 1. Set Up Your Environment

Before deploying, ensure you have a project in Azure AI Foundry and the required permissions.

### 1.1. Create or Select a Project

1. Go to the [Azure AI Foundry portal](https://ai.azure.com){:target="_blank"}.
2. In the left navigation, select **Projects**.
3. Select an existing project or create a new one by selecting **+ New project** and following the prompts.

### 1.2. Check Model Availability

1. In your project, select **Model catalog** from the left menu.
2. Search for **GPT-4o**.
3. Confirm that the model is available for deployment in your region. If not, check your region or contact your administrator.

---

## 2. Deploy the GPT-4o Model

### 2.1. Start the Deployment

1. In the **Model catalog**, select the **GPT-4o** model card.
2. Click **Deploy**.

### 2.2. Configure Deployment Settings

1. **Deployment name**: Enter a unique name for your deployment (e.g., `gpt-4o-prod`).
2. **Deployment type**: Choose between **Serverless API** (pay-per-token) or **Managed compute** (dedicated resources).  
   - *Serverless API* is recommended for most scenarios.
3. **Project**: Select your target project.
4. **Region**: Confirm or select the region for deployment.
5. **Quota**: Ensure you have sufficient quota for the model and deployment type.
6. (Optional) **Advanced settings**: Configure scaling, networking, or authentication as needed.

### 2.3. Review and Deploy

1. Review your settings.
2. Click **Deploy**.

The deployment process may take a few minutes. You can monitor the status in the **Deployments** tab of your project.

---

## 3. Test the Deployment

After deployment, you can test the model directly in the portal or by using the provided endpoint and key.

### 3.1. Test in the Portal

1. Go to your project’s **Deployments** tab.
2. Select your GPT-4o deployment.
3. Use the **Test in Studio** or **Try it** feature to send a prompt and view the response.

### 3.2. Get Endpoint and Key

1. In the deployment details, find the **Endpoint URL** and **API key**.
2. Use these values to call the model from your applications or scripts.

---

## 4. (Optional) Deploy Programmatically

You can also deploy GPT-4o using the Azure AI Foundry Python SDK or Azure CLI. For most users, the portal is the recommended approach.

- For code samples, see [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}.

---

## 5. Clean Up Resources

To avoid unnecessary charges, delete deployments you no longer need:

1. Go to your project’s **Deployments** tab.
2. Select the deployment.
3. Click **Delete**.

---

## Next Steps

- [Use GPT-4o for chat completions in Python](https://learn.microsoft.com/azure/ai-foundry/how-to/use-gpt4o-chat-completions){:target="_blank"}
- [Manage deployments in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/manage-deployments){:target="_blank"}
- [Explore the model catalog in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}

For more information, see the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}.