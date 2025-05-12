# Add Safety Elements After Evaluation with Azure AI Evaluation

## Introduction

This article demonstrates how to add safety elements after evaluating AI model outputs using the Azure AI Evaluation library. You will learn how to apply prompt shields, groundedness checks, custom safety categories, and text moderation to your evaluation workflow. The goal is to help you ensure that your AI model outputs are safe, relevant, and aligned with your requirements.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Evaluation supports authentication using a project connection string and Microsoft Entra ID.

- **Project Connection String**: This string connects your code to a specific Azure AI Foundry project. You can find it in the Azure AI Foundry portal by selecting your project and copying the value from the **Overview** tab under **Project details**.
- **Microsoft Entra ID Authentication**: This method uses your Azure identity to securely access Azure resources. You typically authenticate by running `az login` with the Azure CLI, which allows your code to use your credentials.

To use these methods:

1. Go to the Azure AI Foundry portal.
2. Select your project.
3. Copy the **Project Connection String** from the **Overview** tab.
4. Ensure you have the Azure CLI installed and run `az login` to authenticate with Microsoft Entra ID.

## 2. Developer environment setup

Select your preferred operating system:

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir ai-evaluation-safety
        cd ai-evaluation-safety
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
        pip install azure-ai-evaluation==1.5.0 azure-identity==1.21.0
        ```
    6. Set up environment variables (replace the placeholders with the actual values):
        ```powershell
        $env:PROJECT_CONNECTION_STRING="<your-project-connection-string>"
        $env:AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        $env:AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        $env:AZURE_PROJECT_NAME="<your-project-name>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir ai-evaluation-safety
        cd ai-evaluation-safety
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
        pip install azure-ai-evaluation==1.5.0 azure-identity==1.21.0
        ```
    6. Set up environment variables (replace the placeholders with the actual values):
        ```bash
        export PROJECT_CONNECTION_STRING="<your-project-connection-string>"
        export AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        export AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        export AZURE_PROJECT_NAME="<your-project-name>"
        ```

Replace the placeholders with the actual values from your Azure AI Foundry project.

## 3. Main code components

This section explains how to add safety elements after evaluation using the Azure AI Evaluation library.

### 3.1. Imports and Authentication

You will use the Azure AI Evaluation and Azure Identity libraries to authenticate and access your project.

```python
import os

from azure.ai.evaluation import (
    ContentSafetyEvaluator,
    GroundednessEvaluator,
    CustomCategoryEvaluator,
    TextModerationEvaluator
)
from azure.identity import DefaultAzureCredential
```

### 3.2. Set Up Project and Credentials

Set up your Azure AI project and credentials using environment variables.

```python
azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()
```

### 3.3. Prompt Shields

Prompt shields help detect and block potentially harmful or unsafe prompts before they reach your model.

```python
# Example: Use ContentSafetyEvaluator as a prompt shield
prompt_shield = ContentSafetyEvaluator(
    azure_ai_project=azure_ai_project,
    credential=credential
)

result = prompt_shield(query="Write a story about violence.", response="Once upon a time...")
print("Prompt Shield Result:", result)
```

### 3.4. Groundedness

Groundedness checks ensure that the model's response is based on provided context or source data.

```python
# Example: Use GroundednessEvaluator to check if the response is grounded in the context
groundedness_evaluator = GroundednessEvaluator(
    model_config={"azure_endpoint": "<your-endpoint>", "api_key": "<your-key>", "azure_deployment": "<your-deployment>"}
)
groundedness_result = groundedness_evaluator(
    response="Paris is the capital of France.",
    context="France, a country in Western Europe, has Paris as its capital."
)
print("Groundedness Result:", groundedness_result)
```

### 3.5. Custom Categories

You can define custom categories to flag or filter content based on your organization's needs.

```python
# Example: Use CustomCategoryEvaluator for a custom category
custom_category_evaluator = CustomCategoryEvaluator(
    azure_ai_project=azure_ai_project,
    credential=credential,
    categories=["politics", "medical"]
)
custom_category_result = custom_category_evaluator(
    query="Tell me about the latest political news.",
    response="The election results were announced today."
)
print("Custom Category Result:", custom_category_result)
```

### 3.6. Text Moderation

Text moderation helps detect and filter out inappropriate or unsafe content in model outputs.

```python
# Example: Use TextModerationEvaluator to moderate text
text_moderation_evaluator = TextModerationEvaluator(
    azure_ai_project=azure_ai_project,
    credential=credential
)
moderation_result = text_moderation_evaluator(
    query="What is the capital of France?",
    response="Paris is the capital of France."
)
print("Text Moderation Result:", moderation_result)
```

## 4. Complete code

The following example demonstrates how to add all safety elements after evaluation. Save this code as `add_safety_elements.py`.

```python
"""
Demonstrates how to add safety elements after evaluation using Azure AI Evaluation.
Includes prompt shields, groundedness, custom categories, and text moderation.

Set the following environment variables before running:
- PROJECT_CONNECTION_STRING
- AZURE_SUBSCRIPTION_ID
- AZURE_RESOURCE_GROUP_NAME
- AZURE_PROJECT_NAME
"""

import os

from azure.ai.evaluation import (
    ContentSafetyEvaluator,
    GroundednessEvaluator,
    CustomCategoryEvaluator,
    TextModerationEvaluator
)
from azure.identity import DefaultAzureCredential

def main():
    """
    Run safety evaluations on AI model outputs using various evaluators.
    """
    azure_ai_project = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
        "project_name": os.environ["AZURE_PROJECT_NAME"],
    }
    credential = DefaultAzureCredential()

    # Prompt Shield
    prompt_shield = ContentSafetyEvaluator(
        azure_ai_project=azure_ai_project,
        credential=credential
    )
    prompt_shield_result = prompt_shield(
        query="Write a story about violence.",
        response="Once upon a time..."
    )
    print("Prompt Shield Result:", prompt_shield_result)

    # Groundedness
    groundedness_evaluator = GroundednessEvaluator(
        model_config={
            "azure_endpoint": "<your-endpoint>",
            "api_key": "<your-key>",
            "azure_deployment": "<your-deployment>"
        }
    )
    groundedness_result = groundedness_evaluator(
        response="Paris is the capital of France.",
        context="France, a country in Western Europe, has Paris as its capital."
    )
    print("Groundedness Result:", groundedness_result)

    # Custom Categories
    custom_category_evaluator = CustomCategoryEvaluator(
        azure_ai_project=azure_ai_project,
        credential=credential,
        categories=["politics", "medical"]
    )
    custom_category_result = custom_category_evaluator(
        query="Tell me about the latest political news.",
        response="The election results were announced today."
    )
    print("Custom Category Result:", custom_category_result)

    # Text Moderation
    text_moderation_evaluator = TextModerationEvaluator(
        azure_ai_project=azure_ai_project,
        credential=credential
    )
    moderation_result = text_moderation_evaluator(
        query="What is the capital of France?",
        response="Paris is the capital of France."
    )
    print("Text Moderation Result:", moderation_result)

if __name__ == "__main__":
    main()
```

## 5. How to run the example code

1. Ensure your environment variables are set as described in the developer environment setup.
2. Save the complete code as `add_safety_elements.py`.
3. Run the script:

    ```bash
    python add_safety_elements.py
    ```

## 6. Next steps

- [Azure AI Evaluation documentation](https://aka.ms/azure-ai-evaluation-docs){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-studio/){:target="_blank"}
- [Content Safety in Azure AI](https://learn.microsoft.com/azure/ai-services/content-safety/overview){:target="_blank"}
- [Azure Identity authentication](https://learn.microsoft.com/azure/developer/python/sdk/identity/){:target="_blank"}
- [Azure AI Evaluation samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation/samples){:target="_blank"}